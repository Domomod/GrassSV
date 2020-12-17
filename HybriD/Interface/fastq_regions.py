from ..Region.Load.fastq import FastqInstance
from ..Region.Load.sam import SamInstance
from ..Region.BioRegion import Region

TEXT = 'fastq_regions'


def action(args):
    depth = read_depth_file(args.depth)

    with open(args.fastq1, 'w') as fastq1_file:
        with open(args.fastq2, 'w') as fastq2_file:
            first = None
            for sam in read_sam_file(args.sam):
                if not first:
                    first = sam
                    continue
                second = sam
                for currDepth in depth:
                    if are_good(first, second, currDepth):
                        fastq1_file.write(str(FastqInstance(first.qname, first.seq, first.qual, 1)))
                        fastq2_file.write(str(FastqInstance(second.qname, second.seq, second.qual, 2)))
                        break
                first = sam


def read_depth_file(in_depth: str):
    with open(in_depth) as depth_file:
        return [Region(i.split()[1], i.split()[2], i.split()[0]) for i in depth_file.readlines()]


def read_sam_file(sam_file_name: str):
    for line in open(sam_file_name):
        if line[0] == "@":
            continue
        yield SamInstance(line.split())


def are_good(first, second, depth) -> bool:  # TODO: rename
    same_chromosome = first.rname == depth.name == second.rname
    are_paired = (first.tlen == -second.tlen)
    at_least_one_covered = (depth.start - len(first.seq) <= first.pos <= depth.end) or (depth.start - len(second.seq) <= second.pos <= depth.end)
    at_least_one_unmapped = first.flag & 12 > 1
    return are_paired and ((same_chromosome and at_least_one_covered) or at_least_one_unmapped)


def add_subparser(subparsers):
    fastq_regions = subparsers.add_parser(TEXT, help="Generating fastq regions from sam")
    fastq_regions.add_argument('-f1', '--fastq1', help="Output file number 1", type=str, required=True)
    fastq_regions.add_argument('-f2', '--fastq2', help="Output file number 2", type=str, required=True)
    fastq_regions.add_argument('-s', '--sam', help="Input sam file", type=str, required=True)
    fastq_regions.add_argument('-d', '--depth', help="Input depth file", type=str, required=True)
