import argparse

TEXT = 'find_roi'


def add_subparser(subparsers):
    find_roi = subparsers.add_parser(TEXT, help='finds regions of intrest based on mapping coverage')
    find_roi.add_argument('a', type=str)


def action(args):


    pass
