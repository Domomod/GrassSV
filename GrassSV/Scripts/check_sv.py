#!/usr/bin/python3

import sys

from GrassSV.Alignment.alignments import TranslocationPattern, Pattern, do_they_intersect, sort_coords
from GrassSV.Alignment.load_bed import load_pattern_bed, load_translocations_bed

#import numpy crashes on eagle for some reason
#from GrassSV.Alignment.load_csv import load_regular, load_translocation_as_separate_patterns, load_translocation


def calculate_single_pair(first, second):
    if first.chromosome != second.chromosome:
        return 0
    if not do_they_intersect(first, second):
        return 0  # not intersecting
    outerleft, innerleft, innerright, outerright = sort_coords(first, second)
    sizeOfIntersection = innerright - innerleft
    sizeOfAll=outerright-outerleft
    return sizeOfIntersection / sizeOfAll * 100 if sizeOfAll!=0 else 0


def calculate_type(realtab, simtab, percentage):
    found = 0
    for real in realtab:
        for simulated in simtab:
            if calculate_single_pair(real, simulated) >= percentage:
                found += 1
    return str(found) + "/" + str(len(realtab))


def calculate_pair_of_translocations(first, second, margin):
    destination = calculate_insertions(first.destination, second.destination, margin)
    source = calculate_single_pair(first.source, second.source)
    if destination == True:
        return source
    return 0


def calculate_all_translocations(realtab, simtab, percentage):
    found = 0
    margin = 10
    for real in realtab:
        for simulated in simtab:
            if calculate_pair_of_translocations(real, simulated, margin) >= percentage:
                found += 1
    return str(found) + "/" + str(len(realtab))


def calculate_insertions(first, second, margin):
    if not first.start <= second.start:
        first, second = second, first
    same_chromosome = first.chromosome == second.chromosome
    start_coordinates = abs(first.start - second.start) < margin
    end_coordinates = abs(first.end - second.end) < margin
    return same_chromosome and start_coordinates and end_coordinates


def calculate_all_insertions(realtab, simtab, margin):
    found = 0
    for real in realtab:
        for simulated in simtab:
            if calculate_insertions(real, simulated, margin):
                found += 1
    return str(found) + " / " + str(len(realtab))

def check_sv(generated_dir, detected_dir):

    generated_deletions      = load_pattern_bed(f"{generated_dir}/deletions.bed")
    generated_duplications   = load_pattern_bed(f"{generated_dir}/duplications.bed")
    generated_insertions     = load_pattern_bed(f"{generated_dir}/insertions.bed")
    generated_inversions     = load_pattern_bed(f"{generated_dir}/inversions.bed")
    generated_translocations = load_translocations_bed(f"{generated_dir}/translocations.bed")

    found_deletions      = load_pattern_bed(f"{detected_dir}/deletions.bed")
    found_duplications   = load_pattern_bed(f"{detected_dir}/duplications.bed")
    found_insertions     = load_pattern_bed(f"{detected_dir}/insertion.bed")
    found_inversions     = load_pattern_bed(f"{detected_dir}/filter_inversions.bed")
    found_translocations = load_translocations_bed(f"{detected_dir}/translocations.bed")

    print(f"""### GRASS-SV STATS [Found / Generated] - margin 95
    Deletions : {   calculate_type(generated_deletions     , found_deletions    , 95)}
    Duplications : {calculate_type(generated_duplications  , found_duplications , 80)}
    Insertions : {  calculate_all_insertions(generated_insertions    , found_insertions   , 10)}
    Inversions : {  calculate_type(generated_inversions    , found_inversions   , 95)}
    Translocations : {calculate_all_translocations(generated_translocations, found_translocations, 80)}
    """)