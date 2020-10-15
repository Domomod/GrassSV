import argparse
from HybriD.Scripts import  find_roi
TEXT = 'find_roi'


def add_subparser(subparsers):
    roi = subparsers.add_parser(TEXT, help='finds regions of intrest based on mapping coverage')
    roi.add_argument('input',  type=str)
    roi.add_argument('output', type=str)

    roi.add_argument('limit', type=int)
    roi.add_argument('size', type=int)
    roi.add_argument('margin_size', type=int)

def action(args):
    find_roi.run(input_file=args.input, output_file=args.output, limit_coverage=args.limit, minimum_size=args.size, margin_size=args.margin_size)
