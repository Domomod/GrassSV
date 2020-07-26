from HybriD.Alignment.load_csv import load_regular, load_translocation_as_separate_patterns
from HybriD.Alignment.load_bed import load_pattern_bed


def test_test_breakpoint_coverage_UNOPTIMIZED(regions, mutations):
    covering_region_size_mean = 0
    mutation_count = len(mutations)
    breakpoints = 2*mutation_count
    covered_breakpoints = 0
    both_breakpoints_covered_count = 0

    for mutation in mutations:
        for region in regions:
            left_covered = False
            right_covered = False

            if region.chromosome == mutation.chromosome:
                if region.start < mutation.start < region.end:
                    covering_region_size_mean += (region.end - region.start)
                    covered_breakpoints += 1
                    left_covered = True

                if region.start < mutation.end < region.end:
                    covering_region_size_mean += (region.end - region.start)
                    covered_breakpoints += 1
                    right_covered = True

                if left_covered and right_covered:
                    both_breakpoints_covered_count += 1
                    break

    covering_region_size_mean = covering_region_size_mean / mutation_count

    print(f"{covered_breakpoints}/{breakpoints} breakpoints covered\n"
          f"{both_breakpoints_covered_count}/{mutation_count} mutations have both breakpoints covered\n"
          f"{covering_region_size_mean} is the medium size of breakpoint covering regions")

def test_breakpoint_coverage(regions, mutations):
    regions.sort(key=lambda pattern: (pattern.chromosome, pattern.start))
    mutations.sort(key=lambda pattern: (pattern.chromosome, pattern.start))

    covering_region_size_mean = 0
    breakpoints = 0
    mutation_count = 0
    covered_breakpoints = 0
    both_breakpoints_covered_count = 0

    run_out_of_regions = False
    regions_iter = iter(regions)
    region = next(regions_iter)
    for mutation in mutations:
        left_covered = False
        right_covered = False
        single_breakpoint = False

        mutation_count += 1
        if mutation.start != mutation.end:
            breakpoints += 2
        else:
            single_breakpoint = True
            breakpoints += 1

        if not run_out_of_regions:
            while region.end < mutation.end:
                if region.start < mutation.start < region.end:
                    covering_region_size_mean += (region.end - region.start)
                    covered_breakpoints += 1
                    left_covered = True

                if not single_breakpoint and mutation.start < mutation.end < region.end:
                    covering_region_size_mean += (region.end - region.start)
                    covered_breakpoints += 1
                    right_covered = True
                try:
                    region = next(regions_iter)
                except StopIteration:
                    run_out_of_regions = True
                    break

            if not run_out_of_regions:  # omit if StopIteration encountered
                # last region checked by this mutation, will be the first checked by the next mutation
                if region.start < mutation.start < region.end:
                    covering_region_size_mean += (region.end - region.start)
                    covered_breakpoints += 1
                    left_covered = True

                if not single_breakpoint and region.start < mutation.end < region.end:
                    covering_region_size_mean += (region.end - region.start)
                    covered_breakpoints += 1
                    right_covered = True

                if left_covered and right_covered:
                    both_breakpoints_covered_count += 1

    if mutation_count > 0:
        covering_region_size_mean = covering_region_size_mean / mutation_count

    print(f"{covered_breakpoints}/{breakpoints} breakpoints covered\n"
          f"{both_breakpoints_covered_count}/{mutation_count} mutations have both breakpoints covered\n"
          f"{covering_region_size_mean} is the medium size of breakpoint covering regions")


def load_if_path(path):
    if path != "":
        return load_regular(path)
    else:
        return []


def load_translocation_if_path(path):
    if path != "":
        return load_translocation_as_separate_patterns(path)
    else:
        return []


def run(roi_path, deletion_path, insertion_path, inversion_path, translocation_path, duplication_path):
    regions = load_pattern_bed(roi_path)

    if (deletion_path):
        deletions = load_regular(deletion_path)
        print("\n\nDELETIONS")
        test_test_breakpoint_coverage_UNOPTIMIZED(regions=regions, mutations=deletions)

    if (insertion_path):
        insertions = load_regular(insertion_path)
        print("\n\nINSERTIONS")
        test_test_breakpoint_coverage_UNOPTIMIZED(regions=regions, mutations=insertions)

    if (inversion_path):
        inversions = load_regular(inversion_path)
        print("\n\nINVERSIONS")
        test_test_breakpoint_coverage_UNOPTIMIZED(regions=regions, mutations=inversions)

    if (translocation_path):
        translocations = load_translocation_as_separate_patterns(translocation_path)
        print("\n\nTRANSLOCATIONS")
        test_test_breakpoint_coverage_UNOPTIMIZED(regions=regions, mutations=translocations)

    if (duplication_path):
        duplications = load_regular(duplication_path)
        print("\n\nDUPLICATIONS")
        test_test_breakpoint_coverage_UNOPTIMIZED(regions=regions, mutations=duplications)
