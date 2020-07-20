import argparse
from HybriD.Alignment import  find_sv

TEXT = 'find_sv'


def add_subparser(subparsers):
    find_sv = subparsers.add_parser(TEXT, help='finds structural variations based on contig\'s mappings')
    find_sv.add_argument('alignments', type=str)
    #TODO: implement csv output
    find_sv.add_argument('-c','--csv', type=str, help="saves findings in csv format")
    #TODO: implement bed output
    find_sv.add_argument('-b','--bed', type=str, help="saves findings in bed format")
    #TODO: implement validation
    find_sv.add_argument('--validate', type=str, metavar="path.csv", nargs='+',
                         help="validates findings against supplied mutations")


def action(args):
    find_sv.run(args.alignments)
    pass
