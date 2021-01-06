from typing import *
from enum import Enum

from GrassSV.Alignment.alignments import Alignment, Contig, Pattern


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


def find_alignment_patterns(alignments):
    alignments.sort(key=lambda alignment: (alignment.chromosome, alignment.start))
    insertions = []
    duplications = []
    others = []
    for first, second in pairwise(alignments):
        same_chromosome = second.chromosome == first.chromosome
        if same_chromosome:
            intersecting = second.start < first.end
            adjacent = first.end + 1 == second.start
            if adjacent:
                insertions.append(
                    Pattern(
                        chromosome=first.chromosome,
                        start=first.end,
                        end=second.start,
                        supporting_alignments=[first, second]
                    ))
            elif intersecting:
                duplications.append(
                    Pattern(
                        chromosome=first.chromosome,
                        start=second.start,
                        end=first.end,
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


def filter_inversions(inversion_patterns):
    inversion_patterns.sort(key=lambda alignment: (alignment.chromosome, alignment.start))
    inversions = []
    skip_next = False
    for first_pattern, second_pattern in pairwise(inversion_patterns):
        same_chromosome = second_pattern.chromosome == first_pattern.chromosome
        intersects = second_pattern.start < first_pattern.end
        if same_chromosome and intersects:
            skip_next = True
            inversions.append(
                Pattern(
                    chromosome=first_pattern.chromosome,
                    start=second_pattern.start,
                    end=first_pattern.end,
                    supporting_alignments=first_pattern.supporting_alignments + second_pattern.supporting_alignments
                ))
        elif not skip_next:
            inversions.append(
                first_pattern
            )
        else:
            skip_next = False
    return inversions


def find_duplications(potential_duplications: List[Pattern], alignments: List[Alignment]):
    potential_duplications.sort(key=lambda pattern: (pattern.chromosome, pattern.start))
    alignments.sort(key=lambda alignment: (alignment.chromosome, alignment.start))
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
        supporting_alignments = []
        while interectionPossible:
            alignment = next(alignments_dictionary[potential_duplication.chromosome]["iter"])
            interectionPossible = alignment.start < potential_duplication.end
            if alignment.end > potential_duplication.start:
                intersects = alignment.end < potential_duplication.end \
                             or alignment.start < potential_duplication.end
                if intersects:
                    supporting_alignments.append(alignment)
        pass
