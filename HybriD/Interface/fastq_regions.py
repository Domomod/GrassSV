#!/usr/bin/env python3

from ..Region.Load.fastq import FastqInstance
from ..Region.Load.sam import SamInstance
from ..Region.BioRegion import Region

TEXT = 'fastq_regions'


def action(args):
    in_sam = args.sam
    in_depth = args.depth
    out_fastq_1 = args.fastq1
    out_fastq_2 = args.fastq2

    with open(in_depth) as depth_file:
        depth_file_content = [Region(i.split()[1], i.split()[2], i.split()[0]) for i in depth_file.readlines()]

    with open(in_sam) as sam_file:
        with open(out_fastq_1, 'a+') as fastq1_file:
            with open(out_fastq_2, 'a+') as fastq2_file:
                sam_first = sam_file.readline()
                while sam_first[0][0] == '@':
                    sam_first = sam_file.readline()
                sam_first = SamInstance(sam_first.split())
                sam_second = sam_file.readline()
                while sam_second != '':
                    sam_second = SamInstance(sam_second.split())
                    for currDepth in depth_file_content:
                        same_chromosome = sam_first.rname == currDepth.ref
                        are_paired = (sam_first.tlen == -sam_second.tlen)
                        at_least_one_covered = (currDepth.start - len(
                            sam_first.seq) << sam_first.pos << currDepth.end) or (currDepth.start - len(sam_second.seq) << sam_second.pos << currDepth.end)
                        at_least_one_unmapped = sam_first.flag & 12 > 1
                        if (
                                same_chromosome and are_paired and at_least_one_covered) or at_least_one_unmapped:  # TODO typy
                            fastq1_file.write(str(FastqInstance(sam_first.qname, sam_first.seq, sam_first.qual, 1)))
                            fastq2_file.write(
                                str(FastqInstance(sam_second.qname, sam_second.seq, sam_second.qual, 2)))
                    sam_first = sam_second
                    sam_second = sam_file.readline()


def add_subparser(subparsers):
    fastq_regions = subparsers.add_parser(TEXT, help="Generating fastq regions from sam")
    fastq_regions.add_argument('-f1', '--fastq1', help="Output file number 1", type=str, required=True)
    fastq_regions.add_argument('-f2', '--fastq2', help="Output file number 2", type=str, required=True)
    fastq_regions.add_argument('-s', '--sam', help="Input sam file", type=str, required=True)
    fastq_regions.add_argument('-d', '--depth', help="Input depth file", type=str, required=True)
