from GrassSV.Region import BioRegion
from GrassSV.Region.Load import csv_loader
from GrassSV.Region.Load import zeroCoverage

def match_intersecting_regions(first_records_set, second_records_set, minimal_intersection = 0.0):
    """
    Tets which sequences of first set intersect with any sequence of the other set.
    Matches will be saved in a multidictionary, with first set's sequences being keys to list of matched sequences from the other set.
    @param first_records_set: Set of DNA sequences tested.
    @param second_records_set: Set of DNA sequences matched against first set.
    @param minimal_intersection: Minimal intersection factor to acknowledge the intersection as a significant one. Values <0.0, 1.0>.
    Intersection factor is calulated as: 2 x intersected sequence length / (first sequence length + second sequence length)
    @return: A triple (Matched sequences, First set's unmatched records, Second set's unmatched record)
    """
    minimal_intersection = 0.0

    matched_dict = {}
    unmatched_set_first = []
    unmatched_set_second = []
    for record in first_records_set:
        for other_record in second_records_set:
            if record.intersects(other_record, minimal_intersection):
                if other_record in matched_dict:
                    matched_dict[other_record].append(record)
                else:
                    matched_dict[other_record] = [record, other_record]
                break
            else:
                unmatched_set_first.append(record)
                unmatched_set_second.append(other_record)

    return matched_dict, unmatched_set_first, unmatched_set_second


def visualize_ground_truth_and_prediction():
    regions_of_interest = zeroCoverage.load("data/regions-of-interest/duzyZeroCoverage")

    found_mutations = csv_loader.load_our_finder("data/found-structural-variants/deletions.csv")
    found_mutations += csv_loader.load_our_finder("data/found-structural-variants/insertions.csv")
    found_mutations += csv_loader.load_our_finder("data/found-structural-variants/translocations.csv")

    actual_mutations = csv_loader.load_deletions("data/generated-mutations/deletions.csv")
    actual_mutations += [flattenedVal for translocation in
                         csv_loader.load_translocations("data/generated-mutations/insertions.csv") for
                         flattenedVal in translocation.flatten()]
    actual_mutations += csv_loader.load_inversions("data/generated-mutations/inversions.csv")
    actual_mutations += csv_loader.load_tandem_duplications("data/generated-mutations/tandemDuplications.csv")

    regions_of_interest.sort(key=(lambda record: (record.region.chromosome, record.region.start)))
    found_mutations.sort(key=(lambda record: (record.region.chromosome, record.region.start)))
    actual_mutations.sort(key=(lambda record: (record.region.chromosome, record.region.start)))

    for region in regions_of_interest:
        if region.region.chromosome == "tpg|BK006945.2|":
            print("%s" % region)

    print("\n\n")
    for deletion in found_mutations:
        if deletion.region.chromosome == "tpg|BK006945.2|":
            print("%s" % deletion)

    print("\n\n")
    for deletion in actual_mutations:
        if deletion.region.chromosome == "tpg|BK006945.2|":
            print("%s" % deletion)


def check_svs_detection_accuracy(names, found_svs, actual_deletions, actual_insertions, actual_inversions,
                                 actual_duplications):
    misclasifications = {}
    for name, svs in zip(names, found_svs):
        actually_deletions, *_ = match_intersecting_regions(first_records_set=svs,
                                                            second_records_set=actual_deletions)

        actually_insertions, *_ = match_intersecting_regions(first_records_set=svs,
                                                             second_records_set=actual_insertions)

        actually_inversions, *_ = match_intersecting_regions(first_records_set=svs,
                                                             second_records_set=actual_inversions)

        actually_duplications, *_ = match_intersecting_regions(first_records_set=svs,
                                                               second_records_set=actual_duplications)

        print("\nOut of %d found %s:" % (len(svs), name))
        print("\t%d were truly deletions" % len(actually_deletions))
        print("\t%d were truly insertions" % len(actually_insertions))
        print("\t%d were truly inversions" % len(actually_inversions))
        print("\t%d were truly duplications" % len(actually_duplications))

        misclasifications[name] = {"deletions": actually_deletions,
                                   "insertions": actually_insertions,
                                   "inversions": actually_inversions,
                                   "duplications": actually_duplications}
    return misclasifications


def check_roi_detection_accuracy(deletions, insertions, inversions, duplications, regions_of_interest):
    matched_deletions, *_ = match_intersecting_regions(first_records_set=deletions,
                                                       second_records_set=regions_of_interest)

    print("Out of %d deletions %d appear in detected regions of interest" % (len(deletions), len(matched_deletions)))

    matched_insertions, *_ = match_intersecting_regions(first_records_set=insertions,
                                                        second_records_set=regions_of_interest)

    print("Out of %d insertions %d appear in detected regions of interest" % (len(insertions), len(matched_insertions)))

    matched_inversions, *_ = match_intersecting_regions(first_records_set=inversions,
                                                        second_records_set=regions_of_interest)

    print("Out of %d inversions %d appear in detected regions of interest" % (len(inversions), len(matched_inversions)))

    matched_duplications, *_ = match_intersecting_regions(first_records_set=duplications,
                                                          second_records_set=regions_of_interest)

    print("Out of %d duplications %d appear in detected regions of interest" % (
        len(duplications), len(matched_duplications)))


if __name__ == "__main__":
    actual_deletions = csv_loader.load_deletions("data/generated-mutations/deletions.csv")
    actual_insertions = csv_loader.load_translocations("data/generated-mutations/insertions.csv")
    actual_inversions = csv_loader.load_inversions("data/generated-mutations/inversions.csv")
    actual_duplications = csv_loader.load_tandem_duplications("data/generated-mutations/tandemDuplications.csv")
    roi_names = ["large_mutations_0_cover",
                 "large_mutations_5_cover",
                 "large_mutations_10_cover",
                 "large_mutations_outer_regions"]

    for roi in roi_names:
        regions_of_interest = zeroCoverage.load("data/regions-of-interest/" + roi)

        print(f"""
            \n
            ====================================================================================\n
            ||\t\t\t{roi.upper()}\n
            ====================================================================================\n
            """)
        check_roi_detection_accuracy(deletions=actual_deletions,
                                     insertions=actual_insertions,
                                     inversions=actual_inversions,
                                     duplications=actual_duplications,
                                     regions_of_interest=regions_of_interest)

