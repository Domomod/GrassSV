import argparse

TEXT = 'csv2bed'

def add_subparser(subparsers):
    csv2bed = subparsers.add_parser(TEXT, help='converts sequences from csv format to bed')
    csv2bed.add_argument('-b', type=str, help='help for b')
    csv2bed.add_argument('-c', type=str, action='store', default='', help='test')

def action(args):
    pass