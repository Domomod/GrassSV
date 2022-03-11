import argparse, argcomplete
from enum import Enum
import operator

from ..Region.Load.fastq import FastqInstance
from ..Region.Load.sam import SamInstance
from ..Region.BioRegion import Region

TEXT = 'filter_reads'

class ReadPos(Enum):
    READ_BEFORE = 2
    READ_AFTER = 3
    READ_WITHIN = 4


def add_subparser(subparsers):
    fastq_regions = subparsers.add_parser(TEXT, help="Filter reads by regions of interest")
    fastq_regions.add_argument('-f1', '--fastq1', help="Output file number 1", type=str, required=True)
    fastq_regions.add_argument('-f2', '--fastq2', help="Output file number 2", type=str, required=True)
    fastq_regions.add_argument('-s', '--sam', help="Input sam file", type=str, required=True)
    fastq_regions.add_argument('-roi', '--region-of-interest', help="Input region of interest file", type=str, required=True)


def action(args):
    roi_data_sorted = get_sorted_roi(read_roi_file(args.region_of_interest))
    sam_data = read_sam_file(args.sam)
    sam_data_sorted = sorted(sam_data, key=lambda x: (x.rname, x.pos))
    sam_pairs = {}
    result = {}

    for it in range(0, len(sam_data), 2):
        sam_pairs[sam_data[it]] = sam_data[it+1]
        sam_pairs[sam_data[it+1]] = sam_data[it]
        result[sam_data[it+1]] = False

    sam_data = []

    pos_it = 0
    prev_chrom = "*"
    for record in sam_data_sorted:
        if record.flag & 12 > 1:
            if record in result.keys():
                result[record] = True
            elif record in sam_pairs:
                result[sam_pairs[record]] = True
            continue

        if record.rname != prev_chrom:
            pos_it = 0

        while how_is_positioned(record, roi_data_sorted[record.rname][pos_it]) == ReadPos.READ_BEFORE:
            pos_it += 1

        if how_is_positioned(record, roi_data_sorted[record.rname][pos_it]) == ReadPos.READ_WITHIN:
            if record in result.keys():
                result[record] = True
            elif record in sam_pairs:
                result[sam_pairs[record]] = True
        prev_chrom = record.rname

    with open(args.fastq1, 'w') as fastq1_file:
        with open(args.fastq2, 'w') as fastq2_file:
            for second, v in result.items():
                if (v == True) and (second.rname == sam_pairs[second].rname or second.flag & 12 > 1 or sam_pairs[second].flag & 12 > 1):
                    fastq1_file.write(str(FastqInstance(sam_pairs[second].qname, sam_pairs[second].seq, sam_pairs[second].qual, 1)))
                    fastq2_file.write(str(FastqInstance(second.qname, second.seq, second.qual, 2)))
    

def get_sorted_roi(data):
    result = {}
    for region in data:
        if region.name not in result.keys():
            result[region.name] = []
        result[region.name].append(region)
    for chromosome_name in result.keys():
        result[chromosome_name] = sorted(result[chromosome_name], key=operator.attrgetter('start'))
    return result


def read_roi_file(in_roi: str):
    with open(in_roi) as roi_file:
        return [Region(i.split()[1], i.split()[2], i.split()[0]) for i in roi_file.readlines()]


def read_sam_file(sam_file_name: str):
    res = []
    for line in open(sam_file_name):
        if line[0] == "@":
            continue
        res.append(SamInstance(line.split()))
    return res


def how_is_positioned(sequence, roi):
    if roi.start - len(sequence.seq) <= sequence.pos <= roi.end:
        return ReadPos.READ_WITHIN
    elif roi.start > sequence.pos + len(sequence.seq):
        return ReadPos.READ_AFTER
    else:
        return ReadPos.READ_BEFORE