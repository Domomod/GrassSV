#!/usr/bin/python3

import sys
import pickle
import pprint
import csv
from collections import namedtuple

from GrassSV.Alignment.alignments import TranslocationPattern, Pattern, do_they_intersect, sort_coords, export_records
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


def calculate_misclassified_insertions(generatedtab, foundtab, margin):
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

def calculate_invalid_breakpoint(generated_arr_arr, detected_arr, margin, invalid_arr = None):
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

        if isinvalid == True:
            if invalid_arr is not None:
                invalid_arr.append(found)
            invalid += 1
        
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


def load_structural_variations(directory, sv_types):
    return {sv_type: load_if_exists(f"{directory}/{sv_type}.bed", load_pattern_bed) for sv_type in sv_types}


def bp_mode(generated_dir, detected_dir):
    generated_deletions      = load_if_exists(f"{generated_dir}/deletions.bed", load_pattern_bed)
    generated_insertions     = load_if_exists(f"{generated_dir}/insertions.bed", load_pattern_bed)
    generated_inversions     = load_if_exists(f"{generated_dir}/inversions.bed", load_pattern_bed)
    generated_translocations_f = load_if_exists(f"{generated_dir}/translocations.from.bed", load_pattern_bed)
    generated_translocations_t = load_if_exists(f"{generated_dir}/translocations.to.bed", load_pattern_bed)
    generated_duplications   = load_if_exists(f"{generated_dir}/duplications.bed", load_pattern_bed)
    TotalBreakpoints = 2*len(generated_deletions) + 2*len(generated_inversions)  + \
                       2*len(generated_duplications) + len(generated_insertions) + \
                       3*len(generated_translocations_f)


    print(f"AS          [DEL][INV][DUP][INS][TRN]||[ TP ][ FP ][ FN ]||[Precision][Recall]")
    print(f"BREAKPOINTS [{2*len(generated_deletions):3}][{2*len(generated_inversions):3}][{2*len(generated_duplications):3}][{len(generated_insertions):3}][{3*len(generated_translocations_f):3}]")

    found_breakpoint      = load_pattern_bed(f"{detected_dir}/breakpoints.bed") # this should not fail to load
    if found_breakpoint:

        axis_margin = []
        axis_precision = []
        axis_recall = []
        for margin in range(1,300,10):
                were_deletions      = calculate_breakpoints_classified_as_insertions(generated_deletions     , found_breakpoint, margin)
                were_inversions     = calculate_breakpoints_classified_as_insertions(generated_inversions    , found_breakpoint, margin)
                were_duplications   = calculate_breakpoints_classified_as_insertions(generated_duplications  , found_breakpoint, margin)
                were_translocations = calculate_breakpoints_classified_as_insertions(generated_translocations_f, found_breakpoint, margin)
                were_tr_ins =         calculate_all_insertions(generated_translocations_t, found_breakpoint, margin)
                if 0 != int_or_0(were_translocations) and 0 != int_or_0(were_tr_ins):
                    were_translocations = were_translocations + were_tr_ins #ugly, but will prevent adding strings to ints
                were_insertions     = calculate_all_insertions(generated_insertions, found_breakpoint, margin)
                found_insertions     = load_if_exists(f"{detected_dir}/insertions.bed",     load_pattern_bed)

                TruePositives  = sum([int_or_0(x) for x in [were_deletions, were_inversions, were_duplications, were_translocations, were_insertions]])
                FalsePositives = len(found_breakpoint) - TruePositives
                # FalsePositives = calculate_invalid_breakpoint([generated_deletions, generated_inversions, generated_duplications, generated_translocations_f, generated_translocations_t, generated_insertions], found_breakpoint, margin) + calculate_invalid_breakpoint([generated_deletions, generated_inversions, generated_duplications, generated_translocations_f, generated_translocations_t, generated_insertions], found_insertions, margin)

                FalseNegatives = TotalBreakpoints - TruePositives
                try:
                    Precission = 100 * TruePositives // (TruePositives + FalsePositives)
                except:
                    Precission = 0

                try:
                    Recall     = 100 * TruePositives // (TruePositives + FalseNegatives)
                except:
                    Recall = 0

                axis_precision = axis_precision + [Precission]
                axis_recall = axis_recall + [Recall]
                axis_margin = axis_margin + [margin]

                name = f"BRP - {len(found_breakpoint)}"
                print(f"[{name:10}] {were_deletions:3}, {were_inversions:3}, {were_duplications:3}, {were_insertions:3}, {were_translocations:3} ||[{TruePositives:4}][{FalsePositives:4}][{FalseNegatives:4}]||[{Precission:2}%; {Recall:2}%]")
        
        margin = 100
        invalid_breakpoints = []
        calculate_invalid_breakpoint([generated_deletions, generated_inversions, generated_duplications, generated_translocations_f, generated_translocations_t, generated_insertions], found_breakpoint, margin, invalid_breakpoints)
        calculate_invalid_breakpoint([generated_deletions, generated_inversions, generated_duplications, generated_translocations_f, generated_translocations_t, generated_insertions], found_insertions, margin, invalid_breakpoints)
        export_records(invalid_breakpoints, f"{detected_dir}/invalid_breakpoints.bed")

        print(f"{axis_margin}")
        print(f"{axis_precision}")
        print(f"{axis_recall}")

        sv_detector_name = detected_dir.split('/')[0]
        with open(f"{sv_detector_name}.pickle", 'wb') as file:
            print(f"Saving pickle to {sv_detector_name}.pickle")
            pickle.dump([axis_recall, axis_precision], file, protocol=pickle.HIGHEST_PROTOCOL)
       
        import csv; 
        vectors = zip(axis_margin, axis_precision, axis_recall); 
        with open(f"{sv_detector_name}.csv", 'w', newline='') as f: 
            csv.writer(f).writerows(vectors)

    return

def save_data_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Type', 'Precision', 'Margin', 'Deletions', 'Inversions', 'Duplications', 'Insertions', 'Translocations', 'FalsePositive'])
        for row in data:
            writer.writerow(row)

def save_data_to_pickle(data, filename):
    with open(filename, 'wb') as picklefile:
        pickle.dump(data, picklefile)



# Define constants for precision and margins
PRECISIONS = [99, 95, 80]
MARGINS = [1, 10, 70]
# Define a named tuple for collected data
CollectedData = namedtuple('CollectedData', 'type sub_type deletions inversions duplications insertions translocations false_positive')

def calculate_all(generated, FOUND, precision, margin, specific_calculations=None):
    calculations = {
        'deletions': calculate_type(generated['deletions'], FOUND, precision),
        'inversions': calculate_type(generated['inversions'], FOUND, precision),
        'duplications': calculate_type(generated['duplications'], FOUND, precision),
        'translocations': calculate_type(generated['translocations_separated'], FOUND, precision),
        'insertions': calculate_misclassified_insertions(generated['insertions'], FOUND, margin)
    }

    if specific_calculations:
        calculations.update(specific_calculations)

    return calculations

def process_data(name, calculations, FOUND_len, precision, margin, collected_data):
    false_positive = FOUND_len - sum(map(int_or_0, calculations.values()))
    
    print(f"[{name:10}] {calculations['deletions']:3}, {calculations['inversions']:3}, {calculations['duplications']:3}, {calculations['insertions']:3}, {calculations['translocations']:3}, {false_positive:4}| [prec={precision:2}%; margin={margin:2}bp]")
    collected_data[margin].append(CollectedData(name[:3], name[6:], calculations['deletions'], calculations['inversions'], calculations['duplications'], calculations['insertions'], calculations['translocations'], false_positive))

def process_type(precision, margin, TYPE, FOUND, LEN, generated, collected_data_list):
    calculations = calculate_all(generated, FOUND, precision, margin)
    process_data(TYPE, calculations, LEN, precision, margin, collected_data_list)

def process_found_insertions(precision, margin, TYPE, FOUND, LEN, generated, collected_data_list):
    specific_calculations = {
        'deletions': calculate_breakpoints_classified_as_insertions(generated['deletions'], FOUND, margin),
        'inversions': calculate_breakpoints_classified_as_insertions(generated['inversions'], FOUND, margin),
        'duplications': calculate_breakpoints_classified_as_insertions(generated['duplications'], FOUND, margin),
        'translocations': calculate_breakpoints_classified_as_insertions(generated['translocations_f'], FOUND, margin),
        'trans_ins': calculate_all_insertions(generated['translocations_t'], FOUND, margin),
        'insertions': calculate_all_insertions(generated['insertions'], FOUND, margin)
    }
    if int_or_0(specific_calculations['translocations']) and int_or_0(specific_calculations['trans_ins']):
        specific_calculations['translocations'] += specific_calculations['trans_ins']
        
    process_data(TYPE, specific_calculations, len(FOUND), precision, margin, collected_data_list)

def process_found_translocations(precision, margin, TYPE, FOUND, LEN, generated, collected_data_list):
    specific_calculations = {
        'deletions': " X ",
        'inversions': " X ",
        'duplications': " X ",
        'insertions': " X ",
        'translocations': calculate_all_translocations(generated['translocations'], FOUND, precision, margin)
    }

    process_data(TYPE, specific_calculations, len(FOUND), precision, margin, collected_data_list)

def process_by_type(process_function, found_items, generated, collected_data):
    for precision, margin in zip(PRECISIONS, MARGINS):
        process_function(precision, margin, found_items, generated, collected_data)

def save_collected_data(collected_data, detected_dir):
    for margin in MARGINS:
        csv_filename = f'sv_analysis_margin_{margin}.{detected_dir}.csv'
        pickle_filename = f'sv_analysis_margin_{margin}.{detected_dir}.pkl'
        save_data_to_csv(collected_data[margin], csv_filename)
        save_data_to_pickle(collected_data[margin], pickle_filename)
        
        # Save transposed collected_data
        transposed_data = list(zip(*collected_data[margin]))
        transposed_csv_filename = f'sv_analysis_margin_{margin}_transposed.{detected_dir}.csv'
        transposed_pickle_filename = f'sv_analysis_margin_{margin}_transposed.{detected_dir}.pkl'
        save_data_to_csv(transposed_data, transposed_csv_filename)
        save_data_to_pickle(transposed_data, transposed_pickle_filename)

def check_sv(generated_dir, detected_dir, only_breakpoints):
    if only_breakpoints:
        bp_mode(generated_dir, detected_dir)
        return 0

    found_deletions = load_if_exists(f"{detected_dir}/deletions.bed", load_pattern_bed)
    found_insertions = load_if_exists(f"{detected_dir}/insertions.bed", load_pattern_bed)
    found_inversions = load_if_exists(f"{detected_dir}/inversions.bed", load_pattern_bed)
    found_translocations = load_if_exists(f"{detected_dir}/translocations.bed", load_translocations_bed)
    found_duplications = load_if_exists(f"{detected_dir}/duplications.bed", load_pattern_bed)
    found_bnd = load_if_exists(f"{detected_dir}/bnds.bed", load_pattern_bed)

    SV_TYPE = [f"DEL - {len(found_deletions)}", f"INV - {len(found_inversions)}", f"DUP - {len(found_duplications)}", f"BND - {len(found_bnd)}", f"INS - {len(found_insertions)}", f"TRN - {len(found_translocations)}"]
    SV_FOUND = [found_deletions, found_inversions, found_duplications, found_bnd, found_insertions, found_translocations]
    SV_LENS = [len(found_deletions), len(found_inversions), len(found_duplications), len(found_bnd), len(found_insertions), len(found_translocations)]
    SV_FUNC = [process_type, process_type, process_type, process_type, process_found_insertions, process_found_translocations]

    # Define the generated data dictionary
    generated = {
        'deletions': load_if_exists(f"{generated_dir}/deletions.bed", load_pattern_bed),
        'inversions': load_if_exists(f"{generated_dir}/inversions.bed", load_pattern_bed),
        'duplications': load_if_exists(f"{generated_dir}/duplications.bed", load_pattern_bed),
        'translocations': load_if_exists(f"{generated_dir}/translocations.bed", load_translocations_bed),
        'translocations_separated': load_if_exists(f"{generated_dir}/translocations.bed", load_pattern_bed),
        'translocations_f': load_if_exists(f"{generated_dir}/translocations.bed", load_pattern_bed),
        'translocations_t': load_if_exists(f"{generated_dir}/translocations.to.bed", load_pattern_bed),
        'insertions': load_if_exists(f"{generated_dir}/insertions.bed", load_pattern_bed)
    }

    print(f"            [DEL][INV][DUP][INS][TRN][FalsePositive]")
    print(f"            [{len(generated['deletions']):3}][{len(generated['inversions']):3}][{len(generated['duplications']):3}][{len(generated['insertions']):3}][{len(generated['translocations']):4}]")

    collected_data = {margin: [] for margin in MARGINS}
    for TYPE, FOUND, LEN, process_funtions in zip(SV_TYPE, SV_FOUND, SV_LENS, SV_FUNC):
        if LEN != 0:
            process_by_type(
                lambda precision, margin, found, gen, col: process_funtions(precision, margin, TYPE, FOUND, LEN, generated, col),
                FOUND,
                generated,
                collected_data
            )

    save_collected_data(collected_data, detected_dir.split('/')[0])


def check_sv_benchmark(generated_dir, detected_dir):
    exceptions = []

    benchmark_insertions = load_if_exists(f"{generated_dir}/insertions.bed", load_pattern_bed)
    benchmark_other      = load_if_exists(f"{generated_dir}/deletions.bed", load_pattern_bed)

    found_deletions      = load_if_exists(f"{detected_dir}/deletions.bed",      load_pattern_bed)
    found_insertions     = load_if_exists(f"{detected_dir}/insertions.bed",     load_pattern_bed)
    found_inversions     = load_if_exists(f"{detected_dir}/inversions.bed",     load_pattern_bed)
    found_duplications   = load_if_exists(f"{detected_dir}/duplications.bed",   load_pattern_bed)
    
    #TODO: Check translocations
    #found_translocations_from = load_if_exists(f"{detected_dir}/translocations.bed", load_translocations_bed)
    #found_translocations_to = load_if_exists(f"{detected_dir}/translocations.bed", load_translocations_bed)

    SV_TYPE=[f"DEL - {len(found_deletions)}", f" INV - {len(found_inversions)}", f"DUP - {len(found_duplications)}"]
    SV_FOUND=[found_deletions, found_inversions,  found_duplications]
    SV_LENS = [len(found_deletions), len(found_inversions), len(found_duplications)]


    print(f"            [TruePositive][FalsePositive]")
    for TYPE, FOUND, LEN in zip(SV_TYPE, SV_FOUND, SV_LENS):
        if LEN != 0:
            for prec, margin in zip([99,95,80],[1,10,70]):
                TruePositive = calculate_type(benchmark_other, FOUND, prec)
                FalsePositive = LEN - int_or_0(TruePositive)
                print(f"[{TYPE:10}] {TruePositive:14}, {FalsePositive:14}| [prec={prec:2}%; margin={margin:2}bp]")

    if found_insertions:
        for prec, margin in zip([99,95,80],[1,10,70]):
                TruePositive  = calculate_all_insertions(benchmark_insertions, found_insertions, margin)
                FalsePositive = len(found_insertions) - TruePositive

                name = f"INS - {len(found_insertions)}"
                print(f"[{name:10}] {TruePositive:14}, {FalsePositive:14}| [prec={prec:2}%; margin={margin:2}bp]")
