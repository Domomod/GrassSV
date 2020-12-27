from GrassSV.Alignment.alignment import Alignment, Contig


def load_alignments(path):
    # quast file rows are:
    # 0     1   2   3   4           5       6   7           8
    # S1	E1	S2	E2	Reference	Contig	IDY	Ambiguous	Best_group

    from GrassSV.Region.Load.csv_loader import correct_ref_name
    input = open(path, "r")

    single_alignments = []
    two_alignments_contigs = []
    many_alignments_contigs = []
    alignments = []
    contig = 0
    for line in input:
        line = line.split("\t")
        if (line[0].isnumeric()):
            alignment = Alignment(
                    chromosome = correct_ref_name(line[4]),
                    alignment_start = int(line[0]),
                    alignment_end = int(line[1]),
                    contig_start = int(line[2]),
                    contig_end = int(line[3])
                )

            if(contig != line[5]):
                if len(alignments) == 1:
                    single_alignments.append(alignment)
                elif len(alignments) == 2:
                    two_alignments_contigs.append(
                        Contig(contig, alignments)
                    )
                elif len(alignments) > 2:
                    many_alignments_contigs.append(
                        Contig(contig, alignments)
                    )
                alignments = []

            alignments.append(alignment)
            contig = line[5]

    return [single_alignments, two_alignments_contigs, many_alignments_contigs]
