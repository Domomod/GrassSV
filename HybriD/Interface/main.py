import argparse
from HybriD.Interface import csv2bed, find_sv, find_roi

def run():
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument('--foo', action='store_true', help='help for foo arg.')
    subparsers = parser.add_subparsers(help='help for subcommand', dest='action')

    csv2bed.add_subparser(subparsers)
    find_sv.add_subparser(subparsers)
    find_roi.add_subparser(subparsers)

    args = parser.parse_args()

    if args.action == find_sv.TEXT:
        find_sv.action(args)
    elif args.action == find_roi.TEXT:
        find_roi.action(args)
    elif args.action == csv2bed.TEXT:
        csv2bed.action(args)