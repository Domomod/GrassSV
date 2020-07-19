from typing import List

from HybriD.Detection.Alignment import Alignment
from HybriD.Detection.Pattern import Pattern

downstream = 1
upstream = 0


def asInversionPattern(first_alignment, second_alignment):
    return Pattern(
        chromosome=first_alignment.chromosome,
        start=first_alignment.alignment_start,
        end=second_alignment.alignment_end,
        supporting_alignments=[first_alignment, second_alignment]
    )


def analyzeTwoAlignmentsContigs(contigs):
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

        if not same_chromosome:
            translocation_breakpoints.append(contig)
        else:
            first_before_second = first.alignment_start < second.alignment_start
            if not first_before_second:
                first, second = second, first
                first_before_second = True

            same_direction = (getMappingDirection(first) == getMappingDirection(second))
            if not same_direction:
                inversions.append(asInversionPattern(first, second))
            else:
                both_downstream = getMappingDirection(first)
                if both_downstream:
                    mapped_in_order = first.contig_start < second.contig_start
                    if not mapped_in_order:
                        potential_duplications.append(
                            Pattern(
                                start=first.alignment_start,
                                end=second.alignment_end,
                                chromosome=first.chromosome,
                                supporting_alignments=[first,second]
                            ))
                    else:
                        gap_between = first.alignment_end < second.alignment_start
                        intersecting = first.alignment_end > second.alignment_start
                        if gap_between:
                            deletions.append(contig)
                        elif intersecting:
                            duplication_breakpoints.append(contig)
                        else:
                            insertions.append(contig)
                else:
                    others.append(contig)
    return {"insertions": insertions,
            "inversions": inversions,
            "deletions": deletions,
            "duplication breakpoints": duplication_breakpoints,
            "translocation breakpoints": translocation_breakpoints,
            "potential_duplications": potential_duplications,
            "others": others}


def getMappingDirection(alignment):
    """
    @return: 0 if upstream, 1 if downstream
    """
    return alignment.contig_start < alignment.contig_end


def pairwise(it):
    it = iter(it)
    try:
        this = next(it)
        while True:
            next_val = next(it)
            yield this, next_val
            this = next_val
    except StopIteration:
        # no more elements in the iterator
        return


def analyzeOneAlignmentContigs(alignments):
    alignments.sort(key=lambda alignment: (alignment.chromosome, alignment.alignment_start))
    insertions = []
    duplications = []
    others = []
    for first, second in pairwise(alignments):
        same_chromosome = second.chromosome == first.chromosome
        if same_chromosome:
            intersecting = second.alignment_start < first.alignment_end
            adjacent = first.alignment_end + 1 == second.alignment_start
            if adjacent:
                insertions.append(
                    Pattern(
                        chromosome=first.chromosome,
                        start=first.alignment_end,
                        end=second.alignment_start,
                        supporting_alignments=[first, second]
                    ))
            elif intersecting:
                duplications.append(
                    Pattern(
                        chromosome=first.chromosome,
                        start=second.alignment_start,
                        end=first.alignment_end,
                        supporting_alignments=[first, second]
                    )
                )
            else:
                others.append(first)
        else:
            others.append(first)

    return {
        "insertions": insertions,
        "duplications": duplications,
        "others": others
    }


def analyzeInversions(inversion_patterns):
    inversion_patterns.sort(key=lambda alignment: (alignment.chromosome, alignment.start))
    two_supporting_alignments = []
    one_supporting_alignment = []
    skip_next = False
    for first_pattern, second_pattern in pairwise(inversion_patterns):
        same_chromosome = second_pattern.chromosome == first_pattern.chromosome
        intersects = second_pattern.start < first_pattern.end
        if same_chromosome and intersects:
            skip_next = True
            two_supporting_alignments.append(
                Pattern(
                    chromosome=first_pattern.chromosome,
                    start=second_pattern.start,
                    end=first_pattern.end,
                    supporting_alignments=first_pattern.supporting_alignments + second_pattern.supporting_alignments
                ))
        elif not skip_next:
            one_supporting_alignment.append(
                first_pattern
            )
        else:
            skip_next = False
    return {
        "one supporting alignment": one_supporting_alignment,
        "two supporting alignments": two_supporting_alignments
    }


def searchForDuplications(potential_duplications: List[Pattern], alignments: List[Alignment]):
    potential_duplications.sort(key=lambda pattern: (pattern.chromosome, pattern.start))
    alignments.sort(key=lambda alignment: (alignment.chromosome, alignment.alignment_start))
    alignments_dictionary = {}
    for alignment in alignments:
        if not alignment.chromosome in alignments_dictionary:
            list = []
            list_iter = iter(list)
            alignments_dictionary[alignment.chromosome] = {"iter": list_iter, "list": list}
        alignments_dictionary[alignment.chromosome]["list"].append(alignment)

    for potential_duplication in potential_duplications:
        # Find alignemnts intersecting with potential duplication
        interectionPossible = True
        supporting_alignments=[]
        while interectionPossible:
            alignment = next(alignments_dictionary[potential_duplication.chromosome]["iter"])
            interectionPossible = alignment.alignment_start < potential_duplication.end
            if alignment.alignment_end > potential_duplication.start:
                intersects = alignment.alignment_end < potential_duplication.end \
                             or alignment.alignment_start < potential_duplication.end
                if intersects:
                    supporting_alignments.append(alignment)
        pass