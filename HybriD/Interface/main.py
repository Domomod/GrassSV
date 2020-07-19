import argparse
from HybriD.Temp import csv2bed


def run():
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument('--foo', action='store_true', help='help for foo arg.')
    subparsers = parser.add_subparsers(help='help for subcommand', dest='action')

    csv2bed.add_subparser(subparsers)

    args = parser.parse_args()