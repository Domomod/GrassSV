class Pattern:
    def __init__(self, chromosome, start, end, supporting_alignments=[]):
        self.chromosome = chromosome
        self.start = start
        self.end = end
        self.supporting_alignments = supporting_alignments

    def to_bed(self, name=''):
        return " ".join([self.chromosome, str(self.start), str(self.end)]) + name + '\n'

class ComplexPattern:
    def __init__(self, patterns):
        self.patterns = patterns


def patterns_to_bed(patterns, output_path):
    with open(output_path, "w") as f:
        for pattern in patterns:
            line = pattern.to_bed()
            f.write(line)


def supporting_alignments_to_bed(patterns, output_path):
    with open(output_path, "w") as f:
        for pattern in patterns:
            for alignment in pattern.supporting_alignments:
                line = alignment.to_bed()
                f.write(line)

