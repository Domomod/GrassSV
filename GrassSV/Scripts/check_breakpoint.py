#!/usr/bin/python3

import sys

from GrassSV.Alignment.alignments import TranslocationPattern, Pattern, do_they_intersect, sort_coords
from GrassSV.Alignment.load_bed import load_pattern_bed, load_translocations_bed

#import numpy crashes on eagle for some reason
#from GrassSV.Alignment.load_csv import load_regular, load_translocation_as_separate_patterns, load_translocation


def calculate_single_pair(first, second):
    if first.chromosome != second.chromosome:
        return 0
    if do_they_intersect(first, second):
        return 1  # not intersecting
    return 0

def calculate_all(generated_arr, detected_arr):
    found = 0
    for generated in generated_arr:
        for detected in detected_arr:
            if calculate_single_pair(generated, detected):
                found += 1
                break #One breakpoint is enough evidence



    detected_arr_size = len(detected_arr)
    return f"{found}/{len(generated_arr)}\n"

def calculate_invalid(generated_arr, detected_arr_arr):
    invalid = 0
    for generated in generated_arr:
        isinvalid = True
        for detected_arr in detected_arr_arr:
            for detected in detected_arr:
                if calculate_single_pair(generated, detected):
                    isinvalid = False
                    break #One breakpoint is enough evidence
            if not isinvalid:
                break
        if isinvalid:
            invalid += 1
    return f"{invalid}/{len(generated_arr)}\n"

def check_sv(generated_dir, detected_dir):
    exceptions = []
    generated_tabs = []

    print(f"""### GRASS-SV STATS [Found / Generated] dir: {generated_dir}""")
    try:
        generated_deletions      = load_pattern_bed(f"{generated_dir}/deletions.breakpoints.bed")
        found_deletions      = load_pattern_bed(f"{detected_dir}/breakpoints.bed")
        print(f"""Deletions :      {   calculate_all(generated_deletions     , found_deletions)}""")

        generated_tabs.append(generated_deletions)
    except Exception as e:
        #print(f"""Deletions : failed to calculate, look at the bottom for error log\n""")
        exceptions.append(e)
        pass

    try:
        generated_insertions     = load_pattern_bed(f"{generated_dir}/insertions.breakpoints.bed")
        found_insertions     = load_pattern_bed(f"{detected_dir}/breakpoints.bed")
        print(f"""Insertions :     {  calculate_all(generated_insertions    , found_insertions)}""")

        generated_tabs.append(generated_insertions)
    except Exception as e:
        #print(f"""Insertions : failed to calculate, look at the bottom for error log\n""")
        exceptions.append(e)
        pass

    try:
        generated_inversions     = load_pattern_bed(f"{generated_dir}/inversions.breakpoints.bed")
        found_inversions     = load_pattern_bed(f"{detected_dir}/breakpoints.bed")
        print(f"""Inversions :     {  calculate_all(generated_inversions    , found_inversions)}""")

        generated_tabs.append(generated_inversions)
    except Exception as e:
        #print(f"""Inversions : failed to calculate, look at the bottom for error log\n""")
        exceptions.append(e)
        pass
    
    try:
        generated_translocations = load_pattern_bed(f"{generated_dir}/translocation.breakpoints.bed""")
        found_translocations = load_pattern_bed(f"{detected_dir}/breakpoints.bed")
        print(f"""Translocations : {calculate_all(generated_translocations, found_translocations)}""")

        generated_tabs.append(generated_translocations)
    except Exception as e:
        #print(f"""Translocations : failed to calculate, look at the bottom for error log\n""")
        exceptions.append(e)
        pass
    
    try:
        generated_duplications   = load_pattern_bed(f"{generated_dir}/duplications.breakpoints.bed")
        found_duplications   = load_pattern_bed(f"{detected_dir}/breakpoints.bed")
        print(f"""Duplications :   {calculate_all(generated_duplications  , found_duplications )}""")

        generated_tabs.append(generated_duplications)
    except Exception as e:
        #print(f"""Duplications : failed to calculate, look at the bottom for error log\n""")
        exceptions.append(e)
        pass

    try:
        found_breakpoints   = load_pattern_bed(f"{detected_dir}/breakpoints.bed")
        print(f"""Invalid breakpoints:   {calculate_invalid(found_breakpoints  , generated_tabs )}""")
    except Exception as e:
        #print(f"""Invalid breakpoints : failed to calculate, look at the bottom for error log\n""")
        exceptions.append(e)
        pass


    #for e in exceptions:
        #print(e)
