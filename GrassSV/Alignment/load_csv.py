import os
import pandas

from GrassSV.Alignment.alignments import Pattern
from GrassSV.Alignment.translocation_detect import TranslocationPattern


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
        chromosome = row['Chr'].split('_', 1)[0]
        chromosome = correct_ref_name(chromosome)
        start = row['Start']
        end = row['End']
        region_name = row['Name']

        patterns.append(
            Pattern(
                chromosome=chromosome,
                start=int(start),
                end=int(end)
            ))
    return patterns


def load_translocation(path):
    translocations = []
    data = pandas.read_csv(path, sep='\t')
    for idx, row in data.iterrows():
        chromosome = row['ChrA'].split(' ', 1)[0]
        chromosome = correct_ref_name(chromosome)
        start = row['StartA']
        end = row['EndA']

        first = Pattern(
            chromosome=chromosome,
            start=int(start),
            end=int(end)
        )

        chromosome = row['ChrB'].split(' ', 1)[0]
        chromosome = correct_ref_name(chromosome)
        start = row['StartB']-1
        end = row['StartB']

        second = Pattern(
            chromosome=chromosome,
            start=int(start),
            end=int(end)
        )

        translocations.append(TranslocationPattern(
            source=first,
            destination=second
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
