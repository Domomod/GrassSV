class Pattern:
    def __init__(self, chromosome, start, end, supporting_alignments = []):
        self.chromosome = chromosome
        self.start = start
        self.end = end
        self.supporting_alignments = supporting_alignments

class ComplexPattern:
    def __init__(self, patterns):
        self.patterns = patterns

def patterns_to_bed(patterns, output_path):
    with open(output_path, "w") as f:
        for pattern in patterns:
            line = " ".join([pattern.chromosome, str(pattern.start), str(pattern.end)])
            f.write(line)