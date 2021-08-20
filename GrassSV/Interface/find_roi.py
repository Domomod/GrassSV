import argparse, argcomplete
from GrassSV.Scripts import find_roi

TEXT = 'find_roi'


def add_subparser(subparsers):
    roi = subparsers.add_parser(TEXT, help='finds regions of intrest based on mapping coverage')
    roi.add_argument('input', type=str, help="Depth coverage file")
    roi.add_argument('output', type=str, help="Regions of interest")
    roi.add_argument('limit', type=int, help="Threshold of depth coverage")

    roi.add_argument('-s', '--size', type=int, help="Size of minimal consecutive region", default=1, required=False)
    roi.add_argument('-m', '--margin_size', type=int, help="Size of margins added to the regions", default=150, required=False)


def action(args):
    find_roi.run(input_file=args.input, output_file=args.output, limit_coverage=args.limit, minimum_size=args.size,
                 margin_size=args.margin_size)
