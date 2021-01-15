from typing import *

from GrassSV.Alignment.alignments import Alignment, Pattern, chromosome_position_sort, are_they_adjacent, Insertion

downstream = 1
upstream = 0


def get_mapping_direction(alignment):
    """
    @return: 0 if upstream, 1 if downstream
    """
    return alignment.contig_start < alignment.contig_end


def inversion(first: Alignment, second: Alignment) -> Pattern:
    if not first.start < second.start:
        first, second = second, first
    return Pattern(
        chromosome=first.chromosome,
        start=first.start,
        end=second.end,
        supporting_alignments=[first, second]
    )


def potential_duplication(first: Alignment, second: Alignment) -> Pattern:
    if not first.start < second.start:
        first, second = second, first
    return Pattern(
        start=first.start + 1,
        end=second.end - 1,
        chromosome=first.chromosome,
        supporting_alignments=[first, second]
    )


def potential_deletion(first: Alignment, second: Alignment) -> Pattern:
    if not first.start < second.start:
        first, second = second, first
    return Pattern(
        start=first.end + 1,
        end=second.start - 1,
        chromosome=first.chromosome,
        supporting_alignments=[first, second]
    )


def duplication_breakpoint(first: Alignment, second: Alignment) -> Pattern:
    if not first.start < second.start:
        first, second = second, first
    return Pattern(  # TODO: figure out start and end coordinates
        start=first.start,
        end=second.end,
        chromosome=first.chromosome,
        supporting_alignments=[first, second]
    )


def insertion(first: Alignment, second: Alignment) -> Pattern:
    if not first.start < second.start:
        first, second = second, first
    return Insertion(
        size=abs(first.contig_end - second.contig_start) - (second.start-first.end),
        start=first.end,
        end=second.start,
        chromosome=first.chromosome,
        supporting_alignments=[first, second]
    )


class ContigPatternsData:
    def __init__(self, insertions, inversions, deletions, duplication_breakpoints, translocation_breakpoints,
                 potential_duplications, others):
        self.insertions = insertions
        self.inversions = inversions
        self.deletions = deletions
        self.duplication_breakpoints = duplication_breakpoints
        self.translocation_breakpoints = translocation_breakpoints
        self.potential_duplications = potential_duplications
        self.others = others


def find_contig_patterns(contigs):
    """ Initial step to SV detection. Analizes each contig
    individually, Detect's simple suppaterns.
    which later can be searched for more advanced SVs.
    """
    insertions = []
    inversions = []
    deletions = []
    duplication_breakpoints = []
    translocation_breakpoints = []
    potential_duplications = []
    others = []
    for contig in contigs:
        [first, second] = contig.alignments
        same_chromosome = first.chromosome == second.chromosome
        same_direction = (get_mapping_direction(first) == get_mapping_direction(second))

        if not first.start < second.start and same_chromosome:
            first, second = second, first

        mapped_in_order = first.contig_start < first.contig_end < second.contig_start < second.contig_end or\
                          first.contig_start > first.contig_end > second.contig_start > second.contig_end

        contig_gap = abs(first.contig_end - second.contig_start)
        gap = abs(second.start - first.end)

        gap_between = first.end < second.start
        intersecting = first.end > second.start

        if not same_chromosome:
            translocation_breakpoints.append(contig)
        elif not same_direction:
            inversions.append(
                inversion(first, second))
        elif not mapped_in_order:
            potential_duplications.append(
                potential_duplication(first, second))
        elif contig_gap > gap:
            insertions.append(insertion(first, second))
        elif gap_between:
            deletion = potential_deletion(first, second)
            deletions.append(deletion)
        elif intersecting:
            duplication_breakpoints.append(
                duplication_breakpoint(first, second))
        else:
            others.append(contig)

    return ContigPatternsData(
        insertions=chromosome_position_sort(insertions),
        inversions=chromosome_position_sort(inversions),
        deletions=chromosome_position_sort(deletions),
        duplication_breakpoints=chromosome_position_sort(duplication_breakpoints),
        translocation_breakpoints=translocation_breakpoints, #There is no trivial/useful way to sort translocations
        potential_duplications=chromosome_position_sort(potential_duplications),
        others=chromosome_position_sort(others)
    )
