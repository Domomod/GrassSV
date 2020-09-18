import argparse
from HybriD.Scripts import  find_roi
TEXT = 'find_roi'


def add_subparser(subparsers):
    roi = subparsers.add_parser(TEXT, help='finds regions of intrest based on mapping coverage')
    roi.add_argument('input',  type=str)
    roi.add_argument('output', type=str)
    roi.add_argument('limit', type=int, help='maximum coverage rating for a nucleotide to be in a region')
    roi.add_argument('-m', '--margin', type=int, help='margin size that will be added to region coordinates')

def action(args):
    find_roi.run(input_file=args.input, output_file=args.output, limit_coverage=args.limit)
