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


def calculate_type(generatedtab, foundtab, percentage):
    count_found =0
    if not generatedtab or not foundtab:
        return " X "
    for generated in generatedtab:
        for found in foundtab:
            if calculate_single_pair(generated, found) >= percentage:
                count_found += 1
                break

    foundtab_size = len(foundtab)
    return count_found


def calculate_pair_of_translocations(first, second, margin):
    destination = calculate_insertions(first.destination, second.destination, margin)
    source = calculate_single_pair(first.source, second.source)
    if destination == True:
        return source
    return 0


def calculate_all_translocations(generatedtab, foundtab, percentage, margin):
    if not generatedtab or not foundtab:
        return " X "
    count_found =0
    for generated in generatedtab:
        for found in foundtab:
            if calculate_pair_of_translocations(generated, found, margin) >= percentage:
                count_found += 1
                break

    foundtab_size = len(foundtab)
    invalid = foundtab_size - count_found
    return count_found


def calculate_insertions(first, second, margin):
    if not first.start <= second.start:
        first, second = second, first
    same_chromosome = first.chromosome == second.chromosome
    start_coordinates = abs(first.start - second.start) <= margin
    end_coordinates = abs(first.end - second.end) <= margin
    return same_chromosome and start_coordinates and end_coordinates


def calculate_all_insertions(generatedtab, foundtab, margin):
    if not generatedtab or not foundtab:
        return " X "
    count_found =0
    for generated in generatedtab:
        for found in foundtab:
            if calculate_insertions(generated, found, margin):
                count_found += 1
                break

    foundtab_size = len(foundtab)
    invalid = foundtab_size - count_found
    return count_found

def calculate_insertions(first, second, margin):
    if not first.start <= second.start:
        first, second = second, first
    same_chromosome = first.chromosome == second.chromosome
    start_coordinates = abs(first.start - second.start) <= margin
    end_coordinates = abs(first.end - second.end) <= margin
    return same_chromosome and start_coordinates and end_coordinates


def calculate_misclasified_insertions(generatedtab, foundtab, margin):
    if not generatedtab or not foundtab:
        return " X "
    count_found =0
    for generated in generatedtab:
        for found in foundtab:
            if generated.chromosome == found.chromosome:
                if found.start <= generated.start <= found.end: 
                    if abs(found.start - found.end) <= margin:
                        count_found += 1
                        break

    foundtab_size = len(foundtab)
    invalid = foundtab_size - count_found
    return count_found

def calculate_breakpoints_classified_as_insertions(generatedtab, foundtab, margin):
    if not generatedtab or not foundtab:
        return " X "
    count_found =0
    for generated in generatedtab:
        left_found = False
        right_found = False
        
        for found in foundtab:
            if generated.chromosome == found.chromosome:
                if not left_found and generated.start - margin <= found.start <= generated.end + margin: 
                    if abs(generated.start - found.start) <= margin or abs(found.start - generated.end) <= margin:
                        count_found += 1
                        left_found = True
                elif not right_found and generated.start - margin <= found.end <= generated.end + margin: 
                    if abs(generated.start - found.end) <= margin or abs(found.end - generated.end) <= margin:
                        count_found += 1
                        right_found = True
            if left_found and right_found:
                break


    foundtab_size = len(foundtab)
    invalid = foundtab_size - count_found
    return count_found

def calculate_invalid_breakpoint(generated_arr_arr, detected_arr, margin):
    invalid = 0
    
    for found in detected_arr:
        isinvalid = True
        for generated_arr in generated_arr_arr:
            for generated in generated_arr:
                if generated.chromosome == found.chromosome:
                    if generated.start - margin <= found.start <= generated.end + margin: 
                        if abs(generated.start - found.start) <= margin or abs(found.start - generated.end) <= margin:
                            isinvalid = False
                            break
                    elif generated.start - margin <= found.end <= generated.end + margin: 
                        if abs(generated.start - found.end) <= margin or abs(found.end - generated.end) <= margin:
                            isinvalid = False
                            break
            if isinvalid == False:
                break

        invalid += isinvalid
        
    return invalid


def load_if_exists(dir, function):
    try:
        return function(dir)
    except Exception:
        return []

def int_or_0(val):
    try:
        return int(val)
    except:
        return 0


def bp_mode(generated_dir, detected_dir):
    generated_deletions      = load_if_exists(f"{generated_dir}/deletions.bed", load_pattern_bed)
    generated_insertions     = load_if_exists(f"{generated_dir}/insertions.bed", load_pattern_bed)
    generated_inversions     = load_if_exists(f"{generated_dir}/inversions.bed", load_pattern_bed)
    generated_translocations_f = load_if_exists(f"{generated_dir}/translocations.from.bed", load_pattern_bed)
    generated_translocations_t = load_if_exists(f"{generated_dir}/translocations.to.bed", load_pattern_bed)
    generated_duplications   = load_if_exists(f"{generated_dir}/duplications.bed", load_pattern_bed)

    print(f"AS          [DEL][INV][DUP][INS][TRN][FalsePositive]")
    print(f"BREAKPOINTS [{2*len(generated_deletions):3}][{2*len(generated_inversions):3}][{2*len(generated_duplications):3}][{len(generated_insertions):3}][{3*len(generated_translocations_f):3}]")

    found_breakpoint      = load_pattern_bed(f"{detected_dir}/breakpoints.bed") # this should not fail to load
    if found_breakpoint:
        for prec, margin in zip([99,95,80],[1,10,70]):
                were_deletions      = calculate_breakpoints_classified_as_insertions(generated_deletions     , found_breakpoint, margin)
                were_inversions     = calculate_breakpoints_classified_as_insertions(generated_inversions    , found_breakpoint, margin)
                were_duplications   = calculate_breakpoints_classified_as_insertions(generated_duplications  , found_breakpoint, margin)
                were_translocations = calculate_breakpoints_classified_as_insertions(generated_translocations_f, found_breakpoint, margin)
                were_tr_ins =         calculate_all_insertions(generated_translocations_t, found_breakpoint, margin)
                if 0 != int_or_0(were_translocations) and 0 != int_or_0(were_tr_ins):
                    were_translocations = were_translocations + were_tr_ins #ugly, but will prevent adding strings to ints
                were_insertions     = calculate_all_insertions(generated_insertions, found_breakpoint, margin)

                found_insertions     = load_if_exists(f"{detected_dir}/insertions.bed",     load_pattern_bed)
                FalsePositive = calculate_invalid_breakpoint([generated_deletions, generated_inversions, generated_duplications, generated_translocations_f, generated_translocations_t, generated_insertions], found_breakpoint, margin) - calculate_invalid_breakpoint([generated_deletions, generated_inversions, generated_duplications, generated_translocations_f, generated_translocations_t, generated_insertions], found_insertions, margin)

                name = f"BRP - {len(found_breakpoint)}"
                print(f"[{name:10}] {were_deletions:3}, {were_inversions:3}, {were_duplications:3}, {were_insertions:3}, {were_translocations:3}, {FalsePositive:4}| [prec={prec:2}%; margin={margin:2}bp]")
        

    return

def check_sv(generated_dir, detected_dir, only_breakpoints):
    exceptions = []
    
    if(only_breakpoints):
        bp_mode(generated_dir, detected_dir)
        return 0

    print(f"Loading ground truth ...")
    generated_deletions      = load_if_exists(f"{generated_dir}/benchmark_large_sv_10kbp.bed", load_pattern_bed)
    #generated_deletions      = load_if_exists(f"{generated_dir}/deletions.bed", load_pattern_bed)
    generated_insertions     = load_if_exists(f"{generated_dir}/insertions.bed", load_pattern_bed)
    generated_inversions     = load_if_exists(f"{generated_dir}/inversions.bed", load_pattern_bed)
    generated_translocations = load_if_exists(f"{generated_dir}/translocations.bed", load_translocations_bed)
    generated_duplications   = load_if_exists(f"{generated_dir}/duplications.bed", load_pattern_bed)

    generated_translocations_separated = load_if_exists(f"{generated_dir}/translocations.bed", load_pattern_bed)
    generated_translocations_f = load_if_exists(f"{generated_dir}/translocations.from.bed", load_pattern_bed)
    generated_translocations_t = load_if_exists(f"{generated_dir}/translocations.to.bed", load_pattern_bed)

    print(f"Loading variant calls ...")
    found_deletions      = load_if_exists(f"{detected_dir}/deletions.bed",      load_pattern_bed)
    found_insertions     = load_if_exists(f"{detected_dir}/insertions.bed",     load_pattern_bed)
    found_inversions     = load_if_exists(f"{detected_dir}/inversions.bed",     load_pattern_bed)
    found_translocations = load_if_exists(f"{detected_dir}/translocations.bed", load_translocations_bed)
    found_duplications   = load_if_exists(f"{detected_dir}/duplications.bed",   load_pattern_bed)
    found_bnd            = load_if_exists(f"{detected_dir}/bnds.bed",            load_pattern_bed)

    SV_TYPE=[f"DEL - {len(found_deletions)}", f" INV - {len(found_inversions)}", f"DUP - {len(found_duplications)}", f" BND - {len(found_bnd)}"]
    SV_FOUND=[found_deletions, found_inversions,  found_duplications, found_bnd]
    SV_LENS = [len(found_deletions), len(found_inversions), len(found_duplications), len(found_bnd)]


    print(f"            [DEL][INV][DUP][INS][TRN][FalsePositive]")
    print(f"            [{len(generated_deletions):3}][{len(generated_inversions):3}][{len(generated_duplications):3}][{len(generated_insertions):3}][{len(generated_translocations):4}]")
    for TYPE, FOUND, LEN in zip(SV_TYPE, SV_FOUND, SV_LENS):
        if LEN != 0:
            for prec, margin in zip([99,95,80],[1,10,70]):
                were_deletions      = calculate_type(generated_deletions,    FOUND, prec)
                were_inversions     = calculate_type(generated_inversions,   FOUND, prec)
                were_duplications   = calculate_type(generated_duplications, FOUND, prec)
                were_translocations = calculate_type(generated_translocations_separated, FOUND, prec)
                were_insertions     = calculate_misclasified_insertions(generated_insertions, FOUND, margin)
                FalsePositive = LEN - int_or_0(were_deletions) - int_or_0(were_inversions) - int_or_0(were_duplications) - int_or_0(were_translocations) - int_or_0(were_insertions)

                print(f"[{TYPE:10}] {were_deletions:3}, {were_inversions:3}, {were_duplications:3}, {were_insertions:3}, {were_translocations:3}, {FalsePositive:4}| [prec={prec:2}%; margin={margin:2}bp]")

    if found_insertions:
        for prec, margin in zip([99,95,80],[1,10,70]):
                were_deletions      = calculate_breakpoints_classified_as_insertions(generated_deletions     , found_insertions, margin)
                were_inversions     = calculate_breakpoints_classified_as_insertions(generated_inversions    , found_insertions, margin)
                were_duplications   = calculate_breakpoints_classified_as_insertions(generated_duplications  , found_insertions, margin)
                were_translocations = calculate_breakpoints_classified_as_insertions(generated_translocations_f, found_insertions, margin)
                were_tr_ins =         calculate_all_insertions(generated_translocations_t, found_insertions, margin)
                if 0 != int_or_0(were_translocations) and 0 != int_or_0(were_tr_ins):
                    were_translocations = were_translocations + were_tr_ins #ugly, but will prevent adding strings to ints
                were_insertions     = calculate_all_insertions(generated_insertions, found_insertions, margin)
                FalsePositive = calculate_invalid_breakpoint([generated_deletions, generated_inversions, generated_duplications, generated_translocations_f, generated_translocations_t, generated_insertions], found_insertions, margin)

                name = f"INS - {len(found_insertions)}"
                print(f"[{name:10}] {were_deletions:3}, {were_inversions:3}, {were_duplications:3}, {were_insertions:3}, {were_translocations:3}, {FalsePositive:4}| [prec={prec:2}%; margin={margin:2}bp]")
        
    if found_translocations:
        for prec, margin in zip([99,95,80],[1,10,70]):
                were_deletions      = " X "
                were_inversions     = " X "
                were_duplications   = " X "
                were_insertions     = " X "
                were_translocations = calculate_all_translocations(generated_translocations, found_translocations, prec, margin)
                FalsePositive = len(found_translocations) - int_or_0(were_deletions) - int_or_0(were_inversions) - int_or_0(were_duplications) - int_or_0(were_translocations) - int_or_0(were_insertions)
    
                name = f" TRN - {len(found_translocations)}"
                print(f"[{name:10}] {were_deletions:3}, {were_inversions:3}, {were_duplications:3}, {were_insertions:3}, {were_translocations:3}, {FalsePositive:4}| [prec={prec:2}%; margin={margin:2}bp]")
