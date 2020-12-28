from GrassSV.Region.BioRegion import Region


class SvFinder:
    def __init__(self):
        pass

    def __call__(self, contigs):
        self.insertions = []
        self.inversions = []
        self.deletions = []
        self.duplications = []
        self.translocations = []

        self.single_alignment_contigs = []
        self.multiple_alignments_contigs = []

        self.__split_contigs(contigs)
        self.__analize_single_alignment_contigs()
        self.__analize_multiple_alignment_contigs()

        return self.insertions, self.deletions, self.duplications, self.translocations, self.inversions

    def __split_contigs(self, contigs):
        for contig in contigs:
            if "num_regions" in contig.qualifiers:
                if contig.qualifiers.get("num_regions") == 1:
                    self.single_alignment_contigs.append(contig.region_components[0])
                else:
                    self.multiple_alignments_contigs.append(contig)

    def __analize_single_alignment_contigs(self):
        def is_insertion(contig1, contig2):
            def __check(c1, c2):
                return c1.end - 100 < c1.start < c1.end + 100 \
                       and c2.contig_space_start != 1

            return __check(contig1, contig2) or __check(contig2, contig1)

        for idx in range(len(self.single_alignment_contigs) - 1):
            first_contig = self.single_alignment_contigs[idx]
            second_contig = self.single_alignment_contigs[idx + 1]
            if is_insertion(first_contig, second_contig):
                print(first_contig)
                print(second_contig)
                print("\n\n")

    def __analize_multiple_alignment_contigs(self):
        def are_mapped_on_the_same_chromosome(first_region, second_region):
            return first_region.chromosome == second_region.chromosome

        def get_mapping_distance(first_region, second_region):
            if are_mapped_on_the_same_chromosome(first_region, second_region):
                coordinates = sorted([first_region.start, first_region.end, second_region.start, second_region.end])
                return coordinates[3] - coordinates[0] - first_region.length - second_region.length
            else:
                return "Invalid operation"

        def get_contig_distance(first_region, second_region):
            coordinates = sorted(
                [first_region.contig_space_start, first_region.contig_space_end, second_region.contig_space_start,
                 second_region.contig_space_end])
            return coordinates[3] - coordinates[0] - first_region.length - second_region.length

        def are_mapped_significantly_away(first_region, second_region):
            return get_mapping_distance(first_region, second_region) > get_contig_distance(first_region, second_region)

        def are_intersecting(first_region, second_region):
            return are_mapped_on_the_same_chromosome(first_region, second_region) \
                   and get_mapping_distance(first_region, second_region) < 0

        def is_one_inverted(first_region, second_region):
            return first_region.orientation != second_region.orientation

        for contig in self.multiple_alignments_contigs:
            for first_region, second_region in contig.paired_iter():
                coordinates = sorted(
                    [first_region.start, first_region.end, second_region.start,
                     second_region.end])

                if not are_mapped_on_the_same_chromosome(first_region, second_region):
                    print("Trasnlocataion not implemented yet!\n")

                elif are_intersecting(first_region, second_region):
                    duplication = Region(start=coordinates[1],
                                         end=coordinates[2],
                                         ref=first_region.chromosome,
                                         region_type="duplication",
                                         qualifiers={"supporting_alignments": [contig.name],
                                                     "sv_length": abs(coordinates[1] - coordinates[2])})
                    self.duplications.append(duplication)

                elif is_one_inverted(first_region, second_region):
                    inversion = Region(start=coordinates[1],
                                       end=coordinates[2],
                                       ref=first_region.chromosome,
                                       region_type="inversion",
                                       qualifiers={"supporting_alignments": [contig.name],
                                                   "sv_length": abs(coordinates[1] - coordinates[2])})
                    self.inversions.append(inversion)

                elif are_mapped_significantly_away(first_region, second_region):
                    deletion = Region(start=coordinates[1],
                                      end=coordinates[2],
                                      ref=first_region.chromosome,
                                      region_type="deletion",
                                      qualifiers={"supporting_alignments": [contig.name],
                                                  "sv_length": abs(coordinates[1] - coordinates[2])})
                    self.deletions.append(deletion)
                    """
                    If so happens that between those two regions, somewhere is a region with coverage higher than 0.
                    It is a translocation rather than deletion.
                    """
                else:
                    insertion = Region(start=coordinates[1],
                                       end=coordinates[2],
                                       ref=first_region.chromosome,
                                       region_type="insertion",
                                       qualifiers={"supporting_alignments": [contig.name],
                                                   "sv_length": abs(coordinates[1] - coordinates[2])})
                    self.insertions.append(insertion)


if __name__ == "__main__":
    from GrassSV.Region.Load import quast, csv_loader
    from GrassSV.Region import check_detection_corectness

    contigs = quast.loadContigs(inputFile="data/contigs/from_generated_mutations/all_alignments_contigs.tsv")
    actual_deletions = csv_loader.load_deletions("data/generated-mutations/deletions.csv")
    actual_insertions = csv_loader.load_translocations("data/generated-mutations/insertions.csv")
    actual_inversions = csv_loader.load_inversions("data/generated-mutations/inversions.csv")
    actual_duplications = csv_loader.load_tandem_duplications("data/generated-mutations/tandemDuplications.csv")

    find_structural_variations = SvFinder()
    insertions, deletions, duplications, translocations, inversions = find_structural_variations(contigs)
    names = ["insertions", "deletions", "duplications", "translocations", "inversions"]
    found_svs = [insertions, deletions, duplications, translocations, inversions]

    classification = check_detection_corectness.check_svs_detection_accuracy(names=names,
                                                                             found_svs=found_svs,
                                                                             actual_duplications=actual_duplications,
                                                                             actual_deletions=actual_deletions,
                                                                             actual_insertions=actual_insertions,
                                                                             actual_inversions=actual_inversions)
    pass