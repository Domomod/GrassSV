class Contig:
    def __init__(self, id, alignments):
        self.id = id
        self.alignments = alignments

    def to_bed(self, name = ''):
        return ''.join([alignment.to_bed() for alignment in self.alignments])

class Alignment:
    def __init__(self, chromosome,
                 alignment_start, alignment_end,
                 contig_start, contig_end):
        self.chromosome = chromosome
        self.alignment_start = alignment_start
        self.alignment_end = alignment_end
        self.contig_start = contig_start
        self.contig_end =  contig_end

    def to_bed(self, name = ''):
        return " ".join([self.chromosome, str(self.alignment_start), str(self.alignment_end)]) + name + '\n'

def alignments_to_bed(alignments, output_path):
    with open(output_path, "w") as f:
        for alignment in alignments:
            line = alignment.to_bed()
            f.write(line)