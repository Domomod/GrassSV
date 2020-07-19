import argparse

TEXT = 'find_sv'


def add_subparser(subparsers):
    find_sv = subparsers.add_parser(TEXT, help='finds structural variations based on contig\'s mappings')
    find_sv.add_argument('alignments', type=str)
    find_sv.add_argument('--csv', type=str, help="saves findings in csv format")
    find_sv.add_argument('--bed', type=str, help="saves findings in bed format")
    find_sv.add_argument('--validate', type=str, metavar="path.csv", nargs='+',
                         help="validates findings against supplied mutations")


def action(args):
    pass
