from typing import *


###################################################################################
# Common behaviour
###################################################################################

def SeqUidCounter():
    n = 0
    while True:
        yield n
        n += 1


class ConvertableToBed:
    def to_bed(self, name: str):
        """
        Rewrites record to a bed format
        """

    pass


class SupportConvertableToBed:
    def support_to_bed(self, name: str):
        """
        Rewrites record to a bed format
        """

    pass


###################################################################################
# Contig's and alignments, datatypes representing input data
###################################################################################

class Alignment(ConvertableToBed):
    def __init__(self, chromosome,
                 alignment_start, alignment_end,
                 contig_start, contig_end):
        self.chromosome = chromosome
        self.start = alignment_start
        self.end = alignment_end
        self.contig_start = contig_start
        self.contig_end = contig_end

    def to_bed(self, name: str):
        return " ".join([self.chromosome, str(self.start), str(self.end), name, '\n'])


class Contig(ConvertableToBed):
    def __init__(self, id: int, alignments: List[Alignment]):
        self.id = id
        self.alignments = alignments

    def to_bed(self, name: str):
        return ''.join([alignment.to_bed(f"{self.id}-{i}") for i, alignment in enumerate(self.alignments)])


###################################################################################
# Pattern datatype
###################################################################################

class Pattern(ConvertableToBed, SupportConvertableToBed):
    _gen_uid = SeqUidCounter()

    def __init__(self, chromosome: int, start: int, end: int, supporting_alignments: List[Alignment] = []):
        self.uid = next(Pattern._gen_uid)
        self.chromosome = chromosome
        self.start = start
        self.end = end
        self.size = end - start
        self.supporting_alignments = supporting_alignments

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end and self.chromosome == other.chromosome

    def to_bed(self, name: str):
        return " ".join([self.chromosome, str(self.start), str(self.end), f"{name}-{self.uid}"]) + '\n'

    def support_to_bed(self, name: str):
        return ''.join(
            [alignment.to_bed(f"{name}-{self.uid}-{i}") for i, alignment in enumerate(self.supporting_alignments)])


####################################################################################
# Unique data type required for describing translocation pattern
###################################################################################

class TranslocationPattern(ConvertableToBed, SupportConvertableToBed):
    _gen_uid = SeqUidCounter()

    def __init__(self, source: Pattern, destination: Pattern, support_alignments: List[Alignment] = []):
        self.uid = next(TranslocationPattern._gen_uid)
        self.source = source
        self.destination = destination
        self.supporting_alignments = support_alignments

    def __eq__(self, other):
        return self.source == other.source and self.destination == other.destination

    def to_bed(self, name: str):
        return self.source.to_bed(f"{name}-{self.uid}-source") + self.destination.to_bed(f"{name}-{self.uid}-dest")

    def support_to_bed(self, name: str):
        return ''.join(
            [alignment.to_bed(f"{name}-{self.uid}-{i}") for i, alignment in enumerate(self.supporting_alignments)])


###################################################################################
# Common utilities
###################################################################################

def are_they_adjacent(first: Union[Alignment, Pattern], second: Union[Alignment, Pattern], margin_of_error : int = 0):
    if not first.start < second.start:
        first, second = second, first

    same_chromosome = first.chromosome == second.chromosome
    adjacent = first.end - margin_of_error + 1 <= second.start <= first.end + margin_of_error + 1
    return same_chromosome and adjacent


def do_they_intersect(first: Union[Alignment, Pattern], second: Union[Alignment, Pattern]):
    if not first.start < second.start:
        first, second = second, first

    same_chromosome = first.chromosome == second.chromosome
    intersecting = first.start < second.start < first.end or first.start < second.end < first.end

    return same_chromosome and intersecting


def export_records(alignments: Union[List[ConvertableToBed]], output_path, name='record'):
    with open(output_path, "w") as f:
        for alignment in alignments:
            line = alignment.to_bed(name)
            f.write(line)


def export_supporting_alignments(patterns: List[SupportConvertableToBed], output_path, name='record'):
    with open(output_path, "w") as f:
        for i, pattern in enumerate(patterns):
            out = pattern.support_to_bed(name=name)
            f.write(out)