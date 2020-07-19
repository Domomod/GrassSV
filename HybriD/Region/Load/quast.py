from HybriD.Region.BioRegion import *

def loadContigs(inputFile, contig_filter = lambda contig : True ):
    # quast file rows are:
    # 0     1   2   3   4           5       6   7           8
    # S1	E1	S2	E2	Reference	Contig	IDY	Ambiguous	Best_group

    from HybriD.Region.Load.csv_loader import correct_ref_name

    input = open(inputFile, "r")
    contig_regions = []
    for line in input:
        line = line.split("\t")
        if (line[0].isnumeric()):
            contig_regions.append(
                ContigRegion(
                    start=line[0],
                    end=line[1],
                    ref=correct_ref_name(line[4]),
                    region_type='contig_part',
                    contig_space_start=line[2],
                    contig_space_end=line[3],
                    contig_name=line[5],
                    qualifiers={"IDY": line[6], "Ambiguous": line[7], "Best_group": line[8]}
                )
            )
    input.close()

    contig_regions_grouped = []
    for contig in contig_regions:
        if len(contig_regions_grouped) == 0 or contig.contig_name != contig_regions_grouped[-1][-1].contig_name:
            contig_regions_grouped.append([contig])
        else:
            contig_regions_grouped[-1].append(contig)

    contigs = []
    for regions in contig_regions_grouped:
        contig = Contig(regions=regions, region_name=regions[-1].contig_name, region_type="contig",
                   qualifiers={"num_regions": len(regions)})
        """
        Filter out contigs, unwanted by the user.
        """
        if contig_filter(contig):
            contigs.append(contig)

    return contigs


if __name__ == "__main__":
    test = loadContigs("data/contigs/from_generated_mutations/all_alignments_contigs.tsv")
    for contig in test:
        if(contig.qualifiers.get("num_regions", 1) > 1):
            print(f"{contig.to_str()}\n")
    pass
