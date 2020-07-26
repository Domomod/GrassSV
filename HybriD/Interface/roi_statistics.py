import argparse
from HybriD.Scripts import roi_statistics

TEXT = 'roi_statistics'

def add_subparser(subparsers):
    find_sv = subparsers.add_parser(TEXT, help='finds structural variations based on contig\'s mappings')
    find_sv.add_argument('regions', type=str, metavar='path')
    find_sv.add_argument('-D', '--deletions', type=str, metavar='path')
    find_sv.add_argument('-I', '--insertions', type=str, metavar='path')
    find_sv.add_argument('-d', '--duplications', type=str, metavar='path')
    find_sv.add_argument('-i', '--inversions', type=str, metavar='path')
    find_sv.add_argument('-t', '--translocations', type=str, metavar='path')

def action(args):
    roi_statistics.run(roi_path=args.regions,
                       deletion_path=args.deletions,
                       insertion_path=args.insertions,
                       inversion_path=args.inversions,
                       translocation_path=args.translocations,
                       duplication_path=args.duplications)