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

    with open(in_depth, 'r') as f:
        depth_read = f.readlines()
        depth_read = [i[:-1].split("\t") for i in depth_read]
        depth = [Region(int(i[1]), int(i[2]), i[0]) for i in depth_read]
    with open(in_sam, 'r') as f:
        sam_read = f.readlines()
        sam = [i[:-1].split('\t') for i in sam_read]  # TODO: bardziej skomplikowane wczytywanie
        del sam_read
        sam_instance = []
        for i in sam:
            if i[0][0] != "@":
                sam_instance.append(
                    SamInstance(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11:]))
        del sam

    # zapis do:
    fastq1 = []
    fastq2 = []

    first = sam_instance[0]  # last instance

    for second in sam_instance[1:]:  # s - currnet instance
        for zero in depth:
            if (first.rname == zero.ref and first.tlen == -second.tlen and (
                    (zero.start <= first.pos <= zero.end) or (
                    zero.start <= second.pos <= zero.end))) or (
                    first.flag & 4 == 4 or first.flag & 8 == 8):
                fastq1.append(FastqInstance(first.qname, first.seq, first.qual, 1))
                fastq2.append(FastqInstance(second.qname, second.seq, second.qual, 2))
        first = second

    with open(out_fastq_1, 'w') as f:
        for i in fastq1:
            f.write(str(i))
    with open(out_fastq_2, 'w') as f:
        for i in fastq2:
            f.write(str(i))


def add_subparser(subparsers):
    fastq_regions = subparsers.add_parser(TEXT, help="Generating fastq regions from sam")
    fastq_regions.add_argument('-f1', '--fastq1', help="Output file number 1", type=str, required=True)
    fastq_regions.add_argument('-f2', '--fastq2', help="Output file number 2", type=str, required=True)
    fastq_regions.add_argument('-s', '--sam', help="Input sam file", type=str, required=True)
    fastq_regions.add_argument('-d', '--depth', help="Input depth file", type=str, required=True)

    args = fastq_regions.parse_args()
    action(args)
