import os
import pandas

from HybriD.Alignment.alignment import Alignment
from HybriD.Alignment.pattern import Pattern, ComplexPattern


def correct_ref_name(ref):
    ref = list(ref)
    ref[3] = '|'
    ref[-1] = '|'
    ref = ''.join(ref)
    return ref

def load_regular(path):
    patterns = []
    data = pandas.read_csv(path, sep='\t')
    for idx, row in data.iterrows():
        chromosome = row['Chr'].split(' ', 1)[0]
        chromosome = correct_ref_name(chromosome)
        start = row['Start']
        end = row['End']
        region_name = row['Name']

        patterns.append(
            Pattern(
                chromosome = chromosome,
                start = int(start),
                end = int(end)
            ))
    return patterns

def load_translocation(path):
    translocations = []
    data = pandas.read_csv(path, sep='\t')
    for idx, row in data.iterrows():
        patterns = []
        chromosome = row['ChrA'].split(' ', 1)[0]
        chromosome = correct_ref_name(chromosome)
        start = row['StartA']
        end = row['EndA']

        patterns.append(
            Pattern(
                chromosome = chromosome,
                start = int(start),
                end = int(end)
            ))

        chromosome = row['ChrB'].split(' ', 1)[0]
        chromosome = correct_ref_name(chromosome)
        start = row['StartB']
        end = row['EndB']

        patterns.append(
            Pattern(
                chromosome = chromosome,
                start = int(start),
                end = int(end)
            ))

        translocations.append(ComplexPattern(
            patterns=patterns
        ))
    return translocations

def load_translocation_as_separate_patterns(path):
    patterns = []
    data = pandas.read_csv(path, sep='\t')

    for idx, row in data.iterrows():
        chromosome = row['ChrA'].split(' ', 1)[0]
        chromosome = correct_ref_name(chromosome)
        start = row['StartA']
        end = row['EndA']

        patterns.append(
            Pattern(
                chromosome=chromosome,
                start=int(start),
                end=int(end)
            ))

        chromosome = row['ChrB'].split(' ', 1)[0]
        chromosome = correct_ref_name(chromosome)
        start = row['StartB']
        end = row['EndB']

        patterns.append(
            Pattern(
                chromosome=chromosome,
                start=int(start),
                end=int(end)
            ))
    return patterns