from itertools import combinations
from collections import defaultdict
from venny4py.venny4py import venny4py
import matplotlib.pyplot as plt
from pprint import pprint

from GrassSV.Alignment.load_bed import load_pattern_bed


def is_within_margin(bp1, bp2, margin=70):
    """
    Check if two breakpoints are within the specified margin.
    
    Parameters:
    bp1, bp2: Pattern objects containing breakpoint information.
    margin: The margin within which breakpoints are considered shared.
    
    Returns:
    Boolean indicating whether the breakpoints are within the margin.
    """
    same_chromosome = bp1.chromosome == bp2.chromosome
    within_margin = abs(bp1.start - bp2.start) <= margin
    return same_chromosome and within_margin


def create_combinations_structure():
    """
    Create a dictionary to hold each combination of the 4 sets.
    
    Returns:
    Dictionary with keys as tuples representing combinations of sets and values as empty sets.
    """
    sets = [set1_name, set2_name, set3_name, set4_name]
    combinations_structure = {}

    # Iterate through all possible non-empty combinations of the sets
    for i in range(1, len(sets) + 1):
        for combo in combinations(sets, i):
            key = tuple(sorted(combo))  # Use sorted tuple as the key
            combinations_structure[key] = set()

    return combinations_structure


def DEBUG_fill_with_increment_uuids(combinations_structure):
    """
    Fill the combinations_structure with incremental UIDs for debugging.
    
    Parameters:
    combinations_structure: Dictionary to store the combinations of sets with shared breakpoints.
    """
    counter = 1
    for key in combinations_structure.keys():
        for _ in range(10):  # Up to 10 incrementing integers
            combinations_structure[key].add(counter)
            counter += 1
    pprint(combinations_structure)


def calculate_shared_breakpoints(set1, set2, set3, set4, combinations_structure, margin=10):
    """
    Calculate shared breakpoints within a margin and add them to the combinations_structure.
    
    Parameters:
    set1, set2, set3, set4: Sets containing breakpoints.
    combinations_structure: Dictionary to store the combinations of sets with shared breakpoints.
    margin: The margin within which breakpoints are considered shared.
    
    Returns:
    Updated combinations_structure with shared breakpoints.
    """
    all_breakpoints = {
        set1_name : set1,
        set2_name : set2,
        set3_name : set3,
        set4_name : set4
    }

    for i in range(4, 0, -1):  # Start from combinations of 4 down to 1
        for combo in combinations(all_breakpoints.keys(), i):
            shared_breakpoints = set()

            # Check for breakpoints that are within margin
            for breakpoint in all_breakpoints[combo[0]]:
                if all(any(is_within_margin(breakpoint, bp, margin) for bp in all_breakpoints[set_name]) for set_name in combo[1:]):
                    shared_breakpoints.add(breakpoint)

            if shared_breakpoints:
                key = tuple(sorted(combo))  # Use sorted tuple as the key
                combinations_structure[key].update(shared_breakpoints)

                # Remove these breakpoints from all the original sets to avoid duplication
                for set_name in combo:
                    for bp in list(all_breakpoints[set_name]):
                        if any(is_within_margin(bp, shared_bp, margin) for shared_bp in shared_breakpoints):
                            all_breakpoints[set_name].remove(bp)

    return combinations_structure


def convert_breakpoint_to_uids(combinations_structure):
    """
    Convert breakpoints in combinations_structure to unique incremental integer UIDs.
    
    Parameters:
    combinations_structure: Dictionary to store the combinations of sets with shared breakpoints.
    
    Returns:
    Updated combinations_structure with UIDs.
    """
    uid_counter = 1
    breakpoint_to_uid = {}

    for key, breakpoints in combinations_structure.items():
        uids = set()
        for bp in breakpoints:
            if bp not in breakpoint_to_uid:
                breakpoint_to_uid[bp] = uid_counter
                uid_counter += 1
            uids.add(breakpoint_to_uid[bp])
        combinations_structure[key] = uids

    return combinations_structure


def create_original_sets_from_combinations(combinations_structure):
    """
    Create the original sets from the combinations_structure with UIDs.
    
    Parameters:
    combinations_structure: Dictionary to store the combinations of sets with shared breakpoints.
    
    Returns:
    Dictionary with original sets containing UIDs.
    """
    original_sets = {
        set1_name: set(),
        set2_name: set(),
        set3_name: set(),
        set4_name: set(),
    }


    for combo, uuids in combinations_structure.items():
        for set_name in combo:
            original_sets[set_name].update(uuids)

    return original_sets


set1_name, set2_name, set3_name, set4_name = "GrassSV", "gridss", "pindel", "lumpy"
def plot_venn_diagram(set1, set2, set3, set4):
    """
    Generate a Venn diagram of shared breakpoints from four sets.
    
    Parameters:
    set1_path, set2_path, set3_path, set4_path, ground_truth_path: Paths to the BED files for each set.
    """
    venn_intersection_data = create_combinations_structure()
    # DEBUG_fill_with_increment_uuids(venn_intersection_data) # Either call this or `calculate_shared_breakpoints`
    venn_intersection_data = calculate_shared_breakpoints(set1, set2, set3, set4, venn_intersection_data, margin=70)
    venn_intersection_data = convert_breakpoint_to_uids(venn_intersection_data)
    original_sets = create_original_sets_from_combinations(venn_intersection_data)

    venn_valid = venny4py(original_sets)


def filter_breakpoints_by_ground_truth(bp_set, ground_truth, margin=70):
    valid_bps = set()
    invalid_bps = set()
    for bp in bp_set:
        if any(is_within_margin(bp, gt_bp, margin) for gt_bp in ground_truth):
            valid_bps.add(bp)
        else:
            invalid_bps.add(bp)
    return valid_bps, invalid_bps


def venn_diagram(set1_path, set2_path, set3_path, set4_path, ground_truth_path):
    """
    Generate a Venn diagram of shared breakpoints from four sets.

    Parameters:
    set1_path, set2_path, set3_path, set4_path, ground_truth_path: Paths to the BED files for each set.
    """
    set1 = set(load_pattern_bed(set1_path))
    set2 = set(load_pattern_bed(set2_path))
    set3 = set(load_pattern_bed(set3_path))
    set4 = set(load_pattern_bed(set4_path))
    ground_truth = set(load_pattern_bed(ground_truth_path))

    # Filter breakpoints by ground truth
    set1_valid, set1_invalid = filter_breakpoints_by_ground_truth(set1, ground_truth)
    set2_valid, set2_invalid = filter_breakpoints_by_ground_truth(set2, ground_truth)
    set3_valid, set3_invalid = filter_breakpoints_by_ground_truth(set3, ground_truth)
    set4_valid, set4_invalid = filter_breakpoints_by_ground_truth(set4, ground_truth)

    # Plot Venn diagram for valid sets
    print("Valid breakpoints Venn Diagram")
    plot_venn_diagram(set1_valid, set2_valid, set3_valid, set4_valid)
    plt.title('Valid Breakpoints')
    plt.savefig('valid_breakpoints.png')
    plt.show()

    # Plot Venn diagram for invalid sets
    print("Invalid breakpoints Venn Diagram")
    plot_venn_diagram(set1_invalid, set2_invalid, set3_invalid, set4_invalid)
    plt.title('Invalid Breakpoints')
    plt.savefig('invalid_breakpoints.png')
    plt.show()

# Example usage (replace with actual paths)
# venn_diagram('path_to_grasssv.bed', 'path_to_gridss.bed', 'path_to_pindel.bed', 'path_to_lumpy.bed', 'path_to_ground_truth.bed')
