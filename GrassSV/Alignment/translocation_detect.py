import itertools
from typing import *

from GrassSV.Alignment.alignments import TranslocationPattern, Contig, Alignment, \
    Pattern, do_they_intersect, are_they_adjacent


####################################################################################
# Whole translocation detection pipeline
###################################################################################


####################################################################################
# Filtering out deletions detected as translocations
###################################################################################
class FalseDeletionFilter(object):
    def __call__(self, translocations: List[TranslocationPattern], deletions_unfiltered: List[Pattern]
                 ) -> List[Pattern]:
        deletions = []
        for deletion in deletions_unfiltered:
            is_deletion = True
            i = 0
            for translocation in translocations:
                if do_they_intersect(translocation.source, deletion):
                    is_deletion = False
                    break
            if is_deletion:
                deletions.append(deletion)

        return deletions
####################################################################################
# Filtering translocations based on overlaping of breakpoint contigs and deletions
###################################################################################

class TranslocationDeletionFilter(object):
    def __call__(self, translocation_breakpoints: List[Contig], potential_deletions: List[Pattern]
                 ) -> Tuple[List[TranslocationPattern], List[Pattern], List[Contig]]:
        translocations = []
        breakpoint_not_used = [True] * len(translocation_breakpoints)
        deletions = []
        for deletion in potential_deletions:
            is_deletion = True
            i = 0
            for i, breakpoint in enumerate(translocation_breakpoints):
                if self.is_translocation(breakpoint, deletion):
                    breakpoint_not_used[i] = False
                    if is_deletion:
                        # A translocation can be detected by two breakpoint contigs, writing down both would create a duplicate
                        translocations.append(self.translocation_pattern(breakpoint, deletion))
                    is_deletion = False
                    break
            if is_deletion:
                deletions.append(deletion)

        unused_breakpoints = list(itertools.compress(translocation_breakpoints, breakpoint_not_used))

        return translocations, deletions, unused_breakpoints

    def is_translocation(self, breakpoint: Contig, deletion: Pattern) -> bool:
        self.first, self.second = breakpoint.alignments
        one_intersecting = do_they_intersect(self.first, deletion) or do_they_intersect(self.second, deletion)

        self.intersecting, self.nonintersecting = (self.first, self.second) if do_they_intersect(self.first,
                                                                                                 deletion) else (
            self.second, self.first)
        breakpoints_match = self.intersecting.start == deletion.start or self.intersecting.end == deletion.end

        return one_intersecting and breakpoints_match

    def translocation_pattern(self, breakpoint: Contig, deletion: Pattern):
        if self.intersecting.start == deletion.start:
            start = self.nonintersecting.end
            end = start + 1
        else:
            end = self.nonintersecting.start
            start = end - 1

        destination = Pattern(
            start=start,
            end=end,
            chromosome=self.nonintersecting.chromosome,
        )
        source = deletion

        return TranslocationPattern(
            source=source,
            destination=destination,
            support_alignments=[self.nonintersecting, self.intersecting, *deletion.supporting_alignments]
        )


#############################################################################################################
# Filtering translocations based on adjacency of breakpoint contigs coming from both ends of a translocation
#############################################################################################################

class TranslocationBreakpointFilter(object):
    """
    Detects adjacent alignments coming from to separate contigs, which indicates those contigs
    come from both ends of a translocation. Specifies exact breakpoints of such translocation and
    returns a list found translocations.
    :param breakpoints: Contigs detecting a translocation breakpoint
    :return:
    """

    def __call__(self, breakpoints: List[Contig]) -> Tuple[List[TranslocationPattern], List[Contig]]:
        translocations = []
        leftover_breakpoints = []
        breakpoint_not_used = [True] * len(breakpoints)
        for i, breakpoint in enumerate(breakpoints):
            if breakpoint_not_used[i]:
                    found = False
                    for j, other_breakpoint in enumerate(breakpoints[i::]):
                        if self.is_translocation(breakpoint, other_breakpoint):
                            translocations.append(
                                self.translocation_pattern()
                            )
                            found = True
                            breakpoint_not_used[i + j] = False
                            break
                    if not found:
                        leftover_breakpoints.append(breakpoint)
        return translocations, leftover_breakpoints

    def translocation_pattern(self) -> TranslocationPattern:
        _, destination_start, destination_end, _ = self.sort_alignment_coords(*self.nonadjacent)
        _, source_start, source_end, _ = self.sort_alignment_coords(*self.adjacent)
        destination = Pattern(
            start=destination_start + 1,
            end=destination_end - 1,
            chromosome=self.nonadjacent[0].chromosome
        )

        source = Pattern(
            start=source_start,
            end=source_end,
            chromosome=self.adjacent[0].chromosome
        )

        return TranslocationPattern(
            source=source,
            destination=destination,
            support_alignments=[*self.adjacent, *self.nonadjacent]
        )

    def sort_alignment_coords(self, first: Alignment, second: Alignment) -> Tuple[int, int, int, int]:
        if first.start < second.start:
            return first.start, first.end, second.start, second.end
        else:
            return second.start, second.end, first.start, first.end

    def is_translocation(self, first: Contig, second: Contig) -> bool:
        a, b = self.sort_contig(first)
        c, d = self.sort_contig(second)
        # We don't know apriori which contig could be on which side of translocation
        if are_they_adjacent(a, d, margin_of_error=5):
            self.adjacent = a, d
            self.nonadjacent = b, c
            return True
        elif are_they_adjacent(b, c, margin_of_error=5):
            self.adjacent = b, c
            self.nonadjacent = a, d
            return True
        else:
            return False

    def sort_contig(self, contig: Contig) -> Tuple[Alignment, Alignment]:
        """
        Sorts a contig preserving both alignment direction*1 (3' to 5') or (5' to 3') and contig order.
        Example-Legend: (0<-contig space start, 5<-contig space end)<- alignment
        If a contig is aligned (3' to 5'), returned alignments will appear in regular order.
        Example: (0, 150) (151 300)
        If a contig is aligned (5' to 3'), returned alignments will appear in reversed order.
        Example: (300 151) (150, 0)

        1* Do not confuse with alignment order, which would mean order in which alignments map onto the reference genome
        """
        first, second = contig.alignments
        regular_mapping_direction = first.contig_start < first.contig_end
        if regular_mapping_direction:
            in_order = first.contig_start < second.contig_start # as in (0, 150) (151 300)
        else:
            in_order = first.contig_end > second.contig_end # as in (300 151) (150, 0)

        return (first, second) if in_order else (second, first)
