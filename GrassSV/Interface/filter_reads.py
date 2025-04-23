import argparse#, argcomplete
from enum import Enum
import operator
import os

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
    fastq_regions.add_argument('-ss', '--sam-sorted', help="Input sam file (sorted)", type=str, required=True)
    fastq_regions.add_argument('-roi', '--region-of-interest', help="Input region of interest file", type=str, required=True)


# def print_memory_usage(stage):
#     import psutil
#     process = psutil.Process(os.getpid())
#     print(f"[DEBUG] Memory usage at {stage}: {process.memory_info().rss / (1024 * 1024):.2f} MB")


def action(args):
    # print(f"Reading data")
    # print_memory_usage("start of action")
    roi_data_sorted = get_sorted_roi(read_roi_file(args.region_of_interest))
    # print_memory_usage("after reading ROI file")
    sam_data = read_sam_file(args.sam)
    # print_memory_usage("after reading SAM file")
    sam_data_sorted = read_sam_file(args.sam_sorted) #sorted(sam_data, key=lambda x: (x.rname, x.pos))
    # print_memory_usage("after reading sorted SAM file")
    sam_pairs = {}
    result = {}

    # print(f"Stats")
    # print(f"Roi keys: {roi_data_sorted.keys()}" )
    # print(f"Sam size: {len(sam_data_sorted)}")

    # print(f"Sorting data")
    for it in range(0, len(sam_data), 2):
        sam_pairs[sam_data[it]] = sam_data[it+1]
        sam_pairs[sam_data[it+1]] = sam_data[it]
        result[sam_data[it+1]] = False
    # print_memory_usage("after sorting data")

    sam_data = []

    # print(f"Processing alignments")
    pos_it = 0
    prev_chrom = "*"
    total_records = len(sam_data_sorted)
    processed_records = 0

    for record in sam_data_sorted:
        processed_records += 1
        # print(f"Processed {processed_records}/{total_records} records ({(processed_records / total_records) * 100:.2f}%)")

        if record.flag & 0b1100 > 1:
            if record in result.keys():
                # print(f"result {record} in result.keys()")
                result[record] = True
            elif record in sam_pairs:
                # print(f"result {record} in sam_pairs")
                result[sam_pairs[record]] = True
            continue

        if record.rname != prev_chrom:
            pos_it = 0

        if record.rname not in roi_data_sorted:
            #print(f"[INFO] There is no '{record.rname}' in roi dictionary")
            continue #There is no roi for this chromosome

        #this is for debugging atm, remove later and call directly
        roi_on_current_chromosome=roi_data_sorted[record.rname]

        while how_is_positioned(record, roi_on_current_chromosome[pos_it]) == ReadPos.READ_BEFORE:
            if pos_it + 1 >= len(roi_on_current_chromosome): #This covers case when there are still reads that are positioned before last roi in current chromosome 
                break
            pos_it += 1
            #print(f"roi( {roi_on_current_chromosome[pos_it].to_str()} ) || sam ( {record} )")
            #print(f"record.rname( {record.rname} ) pos_it( {pos_it} )")
        

        if how_is_positioned(record, roi_on_current_chromosome[pos_it]) == ReadPos.READ_WITHIN:
            if record in result.keys():
                result[record] = True
            elif record in sam_pairs:
                result[sam_pairs[record]] = True
        prev_chrom = record.rname
    # print_memory_usage("after processing alignments")

    # print(f"Filtering reads")
    with open(args.fastq1, 'w') as fastq1_file:
        with open(args.fastq2, 'w') as fastq2_file:
            for second, is_marked_for_export in result.items():
                same_chromosome = (second.rname == sam_pairs[second].rname)
                one_or_the_other_unmapped = (second.flag & 12 > 1 or sam_pairs[second].flag & 12 > 1)
                # if is_marked_for_export:
                #     print(f"{second}\nis_marked_for_export={is_marked_for_export}")
                #     print(f"same_chromosome={same_chromosome}")
                #     print(f"one_or_other_unmapped={one_or_the_other_unmapped}")
                #     print(f"overall={(is_marked_for_export) and ( same_chromosome or one_or_the_other_unmapped)}")

                if (is_marked_for_export) and ( same_chromosome or one_or_the_other_unmapped):
                    fastq1_file.write(str(FastqInstance(sam_pairs[second].qname, sam_pairs[second].seq, sam_pairs[second].qual, 1)))
                    fastq2_file.write(str(FastqInstance(second.qname, second.seq, second.qual, 2)))
    # print_memory_usage("end of action")


def get_sorted_roi(data):
    # print_memory_usage("start of get_sorted_roi")
    result = {}
    for region in data:
        if region.name not in result.keys():
            result[region.name] = []
        result[region.name].append(region)
    # roi should already be sorted
    for chromosome_name in result.keys():
       result[chromosome_name] = sorted(result[chromosome_name], key=operator.attrgetter('start'))
    # print_memory_usage("end of get_sorted_roi")
    return result


def read_roi_file(in_roi: str):
    # print_memory_usage("start of read_roi_file")
    with open(in_roi) as roi_file:
        data = [Region(i.split()[1], i.split()[2], i.split()[0]) for i in roi_file.readlines()]
    # print_memory_usage("end of read_roi_file")
    return data


def read_sam_file(sam_file_name: str):
    # print_memory_usage("start of read_sam_file")
    res = []
    for line in open(sam_file_name):
        if line[0] == "@":
            continue
        res.append(SamInstance(line.split()))
    # print_memory_usage("end of read_sam_file")
    return res


def how_is_positioned(sequence, roi):
    if roi.start - len(sequence.seq) <= sequence.pos <= roi.end:
        return ReadPos.READ_WITHIN
    elif roi.start > sequence.pos + len(sequence.seq):
        return ReadPos.READ_AFTER
    else:
        return ReadPos.READ_BEFORE
