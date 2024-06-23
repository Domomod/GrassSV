from itertools import combinations
from collections import defaultdict
from venny4py.venny4py import *
import matplotlib.pyplot as plt

from GrassSV.Alignment.alignments import Pattern
from GrassSV.Alignment.load_bed import load_pattern_bed

# Function to check if two breakpoints are within the margin
def is_within_margin(bp1, bp2, margin=70):
    same_chromosome = bp1.chromosome == bp2.chromosome
    within_margin = abs(bp1.start - bp2.start) <= margin
    return same_chromosome and within_margin

# Function to find common breakpoints across sets
def find_common_breakpoints(sets, margin=70):
    breakpoint_map = defaultdict(set)
    all_breakpoints = set()

    for set_name, bp_set in sets.items():
        for bp in bp_set:
            all_breakpoints.add(bp)
            for other_bp in all_breakpoints:
                if is_within_margin(bp, other_bp, margin):
                    breakpoint_map[other_bp].add(set_name)
                    breakpoint_map[bp].add(set_name)
    
    return breakpoint_map

# Function to prepare data for the Venn diagram
def prepare_venn_data(breakpoint_map, set_names):
    venn_data = {name: set() for name in set_names}

    for bp, set_name in breakpoint_map.items():
        for name in set_name:
            venn_data[name].add(bp)
    
    return venn_data

def venn_diagram(set1_path, set2_path, set3_path, set4_path):
    set1 = set(load_pattern_bed(set1_path))
    set2 = set(load_pattern_bed(set2_path))
    set3 = set(load_pattern_bed(set3_path))
    set4 = set(load_pattern_bed(set4_path))

    sets = {
        'GrassSV' : set1,
        'Gridss'  : set2,
        'Pindel'  : set3,
        'Lumpy'   : set4
    }

    # Find common breakpoints
    breakpoint_map = find_common_breakpoints(sets)

    # Prepare data for the Venn diagram
    venn_data = prepare_venn_data(breakpoint_map, sets.keys())

    # Convert Pattern objects to strings for venny4py
    venn_data_str = {key: {str(bp) for bp in value} for key, value in venn_data.items()}


    # Generate the Venn diagram
    venn = venny4py(venn_data_str)


# Example usage
# venn_diagram('set1.bed', 'set2.bed', 'set3.bed', 'set4.bed')
