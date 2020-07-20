class Contig:
    def __init__(self, id, alignments):
        self.id = id
        self.alignments = alignments

class Alignment:
    def __init__(self, chromosome,
                 alignment_start, alignment_end,
                 contig_start, contig_end):
        self.chromosome = chromosome
        self.alignment_start = alignment_start
        self.alignment_end = alignment_end
        self.contig_start = contig_start
        self.contig_end =  contig_end