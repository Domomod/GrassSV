import itertools
from typing import *

from GrassSV.Alignment.alignments import TranslocationPattern, Contig, Alignment, \
    Pattern, do_they_intersect, are_they_adjacent, sort_coords, are_they_identical, same_chromosome


####################################################################################
# Whole translocation detection pipeline
###################################################################################

class TranslocationFilter(object):
    def __call__(self, deletions: List[Pattern], translocation_breakpoints: List[Contig],
                 duplications: List[Pattern]):
        same_chromosome_filter = SingleChromosomeTranslocationFilter()
        breakpoint_filter = TranslocationBreakpointFilter()
        deletion_breakpoint_filter = TranslocationDeletionFilter()
        remove_misclasified_deletions = MisclassifiedDeletionFilter()

        translocations0, deletions, duplications = same_chromosome_filter(deletions, duplications)
        translocations1, unused_breakpoints = breakpoint_filter(translocation_breakpoints)
        translocations2, deletions, unused_breakpoints = deletion_breakpoint_filter(unused_breakpoints, deletions)
        translocations = translocations0 + translocations1 + translocations2
        deletions = remove_misclasified_deletions(translocations, deletions)
        return translocations, deletions, unused_breakpoints, duplications


#############################################################################################################
# Filtering translocations taking place on a single chromosome
#############################################################################################################

class SingleChromosomeTranslocationFilter(object):
    """
    First detects adjacent deletion patterns indicating a single chromosme translocation took place.
    Second detects a potential duplication pattern caused by the detected translocation and filters it out.
    Returns detected translocation, unused deletions and unused potential_duplications.
    """

    def __call__(self, deletions: List[Pattern], duplications: List[Pattern]):
        self.translocations = []
        self.helper_patterns = []

        deletions = self.find_deletion_only_patterns(deletions)
        deletions = self.find_deletion_duplication_pattern(deletions, duplications)
        duplications = self.remove_mismatched_duplications(duplications)

        return self.translocations, deletions, duplications

    def find_deletion_only_patterns(self, deletions: List[Pattern])\
            ->List[Pattern]:
        """
        Looks through the list of deletions to find, ones adjacent to each other.
        Due to possible imperfections in mapping's, contig assembly or sequencing, an margin
        of error is applied to the adjacency relation.
        Deletions adjacent to each other are caused by same chromosome translocations, otherwise
        they would be detected as a single deletion.
        Returns unused deletions, and appends detected translocations to a member variable
        """
        unused_deletions = []
        deletion_not_used = [True] * len(deletions)

        last_iteration_succesfull = False
        for i, deletion in enumerate(deletions[:-1]):
            if deletion_not_used[i]:
                succes = False
                for j, other_deletion in enumerate(deletions[i + 1:]):
                    if are_they_adjacent(deletion, other_deletion, margin_of_error=10):
                        self.helper_patterns.append(
                            self.helper_pattern(deletion, other_deletion)
                        )
                        self.translocations.append(
                            self.make_translocation_from_deletions(deletion, other_deletion)
                        )
                        deletion_not_used[i + j + 1] = False
                        succes = True
                        break

                if not succes:
                    unused_deletions.append(deletion)

        if last_iteration_succesfull == False:
            unused_deletions.append(deletions[-1])

        return unused_deletions

    def find_deletion_duplication_pattern(self, deletions : List[Pattern], duplications : List[Pattern])\
            ->List[Pattern]:
        """
        Looks for deletion and duplication pairs that share their left or right coordinate (with a small margin of
        error). Such occuring indicates a translocation took place.
        Returns unused deletions, and appends detected translocations to a member variable
        """
        unused_deletions = []
        for deletion in deletions:
            found = False
            for duplication in duplications:
                if deletion.start <= duplication.start <= deletion.end \
                        or duplication.start <= deletion.start <= duplication.end:
                    left, inner_left, inner_right, right = sort_coords(deletion, duplication)
                    if left-3 <= inner_left <= left+3:
                        found = True
                        inner = inner_right
                    elif right-3 <= inner_right <= right+3:
                        found = True
                        inner = inner_left
                    if found:
                        pattern = \
                            self.make_translocation_from_deletion_duplication(
                                left, inner, right,
                                deletion=deletion, duplication=duplication)
                        self.translocations.append(pattern)
                        self.helper_patterns.append(
                            Pattern(start=left, end=right, chromosome=deletion.chromosome))
                        break
            if not found:
                unused_deletions.append(deletion)
        return unused_deletions

    def remove_mismatched_duplications(self, duplications:List[Pattern])\
            ->List[Pattern]:
        """
        Some duplication patterns take a role in detecting of translocations, therefore they have to be
        filtered out. In this case they are filtered out by searching for a single chromosome translocation
        with identical left-most and right-most coordinates (with a small margin of error).
        Returns filtered duplications
        """
        unused_duplications = []
        for potential_duplication in duplications:
            used = False
            for translocation in self.helper_patterns:
                if are_they_identical(translocation, potential_duplication, margin_of_error=10):
                    used = True
                    translocation.supporting_alignments.append(potential_duplication)
            if not used:
                unused_duplications.append(potential_duplication)
        return unused_duplications


    def helper_pattern(self, deletion: Pattern, other_deletion: Pattern) -> Pattern:
        """
        Creates a helper pattern. Used to filter out duplication pattern's caused by translocations.
        """
        start, _, _, end = sort_coords(deletion, other_deletion)
        return Pattern(
            start=start,
            end=end,
            chromosome=deletion.chromosome
        )

    def make_translocation_from_deletions(self, deletion: Pattern, other_deletion: Pattern) -> TranslocationPattern:
        first, second, third, fourth = sort_coords(deletion, other_deletion)
        if second - first < fourth - third:
            return TranslocationPattern(
                source=Pattern(
                    start=first,
                    end=second,
                    chromosome=deletion.chromosome
                ),
                destination=Pattern(
                    start=fourth,
                    end=fourth + 1,
                    chromosome=deletion.chromosome
                ),
                support_alignments=[*deletion.supporting_alignments, *other_deletion.supporting_alignments]
            )
        else:
            return TranslocationPattern(
                source=Pattern(
                    start=third,
                    end=fourth,
                    chromosome=deletion.chromosome
                ),
                destination=Pattern(
                    start=first - 1,
                    end=first,
                    chromosome=deletion.chromosome
                ),
                support_alignments=[*deletion.supporting_alignments, *other_deletion.supporting_alignments]
            )

    def make_translocation_from_deletion_duplication(self, first: int, second: int, third: int, deletion: Pattern,
                                                     duplication: Pattern) -> TranslocationPattern:
        if second - first < third - second:
            source_start = first
            source_end = second
            destination_start = third
            destination_end = third + 1

        else:
            source_start = second
            source_end = third
            destination_start = first - 1
            destination_end = first

        return TranslocationPattern(
            source=Pattern(
                start=source_start,
                end=source_end,
                chromosome=deletion.chromosome
            ),
            destination=Pattern(
                start=destination_start,
                end=destination_end,
                chromosome=deletion.chromosome
            ),
            support_alignments=[deletion, duplication, *deletion.supporting_alignments,
                                *duplication.supporting_alignments]
        )


#############################################################################################################
# Filtering translocations based on adjacency of breakpoint contigs coming from both ends of a translocation
#############################################################################################################

class TranslocationBreakpointFilter(object):
    """
    Detects adjacent alignments coming from to separate contigs, which indicates those contigs
    come from both ends of a translocation. Specifies exact breakpoints of such translocation and
    returns a list of found translocations.
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
                for j, other_breakpoint in enumerate(breakpoints[i + 1:]):
                    if self.is_translocation(breakpoint, other_breakpoint):
                        translocation = self.translocation_pattern()
                        translocations.append(translocation)
                        found = True
                        breakpoint_not_used[i + j] = False
                        break
                if not found:
                    leftover_breakpoints.append(breakpoint)
        return translocations, leftover_breakpoints

    def translocation_pattern(self) -> TranslocationPattern:
        destination_start, _, _, destination_end = sort_coords(*self.adjacent)
        _, source_start, source_end, _ = sort_coords(*self.nonadjacent)
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

    def is_translocation(self, first: Contig, second: Contig) -> bool:
        a, b = self.sort_contig(first)
        c, d = self.sort_contig(second)
        # We don't know apriori which contig could be on which side of translocation
        if are_they_adjacent(a, d, margin_of_error=10) and same_chromosome(b, c):
            self.adjacent = a, d
            self.nonadjacent = b, c
            return True
        elif are_they_adjacent(b, c, margin_of_error=10) and same_chromosome(a, d):
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
            in_order = first.contig_start < second.contig_start  # as in (0, 150) (151 300)
        else:
            in_order = first.contig_end > second.contig_end  # as in (300 151) (150, 0)

        return (first, second) if in_order else (second, first)


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


####################################################################################
# Filtering out deletions detected as translocations
###################################################################################

class MisclassifiedDeletionFilter(object):
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
