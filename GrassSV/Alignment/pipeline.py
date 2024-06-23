from typing import *
from itertools import groupby
from enum import Enum

from GrassSV.Alignment.alignments import Alignment, Contig, Pattern, are_they_adjacent


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

def combination(it, r):
    if r:
        for i in range(r - 1, len(it)):
            for cl in combination(it[:i], r - 1):
                yield cl + (it[i],)
    else:
        yield tuple()


def find_alignment_patterns(alignments):
    alignments.sort(key=lambda alignment: (alignment.chromosome, alignment.start))

    insertions = []
    duplications = []
    others = []
    for first, second in pairwise(alignments):
        same_chromosome = second.chromosome == first.chromosome
        if same_chromosome:
            if are_they_adjacent(first, second, margin_of_error=3):
                pattern = Pattern(
                        chromosome=first.chromosome,
                        start=first.end,
                        end=second.start,
                        supporting_alignments=[first, second]
                    )
                insertions.append(pattern)
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
    inversions = []
    skip_next = False

    for chromosome, iterator in groupby(inversion_patterns, key= lambda x : x.chromosome):
        iterations_grouped_by_chromosome = list(iterator)
        for first, second in combination(iterations_grouped_by_chromosome, 2):
            # Sanitize data
            first.start, first.end = sorted([first.start, first.end])
            second.start, second.end = sorted([second.start, second.end])
            # Sorting so the overlap calculation is easier 
            first, second = sorted([first, second], key=lambda x : x.start)
            overlap_exists = not (first.end < second.start or second.end < first.start)
            union_start , overlap_start, overlap_end, union_end = sorted([first.start, first.end, second.start, second.end])
            virtually_identical = 0.95 < (overlap_end - overlap_start) / (union_end - union_start)
            if overlap_exists and virtually_identical:
                inversions.append(
                    Pattern(
                        chromosome=first.chromosome,
                        start=overlap_start,
                        end=overlap_end,
                        supporting_alignments=first.supporting_alignments + second.supporting_alignments
                    ))

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
