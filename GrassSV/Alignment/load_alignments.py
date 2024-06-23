from GrassSV.Alignment.alignments import Alignment, Contig
import os


def load_alignments(path):
    # quast file rows are:
    # 0     1   2   3   4           5       6   7           8
    # S1	E1	S2	E2	Reference	Contig	IDY	Ambiguous	Best_group

    from GrassSV.Region.Load.csv_loader import correct_ref_name
    input = open(path, "r")

    print(f"""
    ========= OPENED ALIGNMENTS FILE ==================
    File path: {path}
    File size: {os.path.getsize(path)}
    """)
    
    single_alignments = []
    two_alignments_contigs = []
    many_alignments_contigs = []
    alignments = []
    contig = 0
    for line in input:
        line = line.split("\t")

        #This is a fix for the sacharomytes yeast genome
        def correct_ref_name(ref):
            ref = list(ref)
            ref[3] = '|'
            ref[-1] = '|'
            ref = ''.join(ref)
            return ref

        if (line[0].isnumeric()):
            alignment = Alignment(
                    chromosome = correct_ref_name(line[4]),
                    alignment_start = int(line[0]),
                    alignment_end = int(line[1]),
                    contig_start = int(line[2]),
                    contig_end = int(line[3]),
                    contig_name= line[5]
                )

            if(contig != line[5]):
                if len(alignments) == 1:
                    single_alignments.append(alignment)
                elif len(alignments) == 2:
                    two_alignments_contigs.append(
                        Contig(contig, alignments)
                    )
                elif len(alignments) > 2:
                    for first, second in zip(alignments[:-1], alignments[1:]):
                        two_alignments_contigs.append(
                            Contig(contig, [first, second])
                        )
                alignments = []

            alignments.append(alignment)
            contig = line[5]
    
    print(f""""
    ===LOADED CONTIGS PER NUMBER OF ALIGNMENTS TABLE===
    single alignment | two_alignments | many_alignments
    {len(single_alignments):17}|{len(two_alignments_contigs):16}|{len(many_alignments_contigs):16}
    
    """)
            
    return [single_alignments, two_alignments_contigs, many_alignments_contigs]
