import argparse

from HybriD.Scripts import generated_mutations_to_bed

TEXT = 'csv2bed'


def add_subparser(subparsers):
    csv2bed = subparsers.add_parser(TEXT, help='converts sequences from csv format to bed')
    csv2bed.add_argument('-b', '--bed', type=str, metavar='path', help='output file', required=True)
    csv2bed.add_argument('-c', '--csv', type=str, metavar='path', nargs='+', help='input file[files]', action='store',
                         default='', required=True)


def action(args):
    print(args.csv)
    generated_mutations_to_bed.run(bed_path=args.bed,
                                   csv_paths=args.csv)
