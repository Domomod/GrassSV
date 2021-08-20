import argparse, argcomplete

from GrassSV.Alignment import load_alignments

TEXT = 'quast2bed'

def add_subparser(subparsers):
    csv2bed = subparsers.add_parser(TEXT, help='converts sequences from quast tsv format to bed',
                                    description="Convert alignments produced by quast from tsv format to bed, for later visualization")
    csv2bed.add_argument('-i', '--input', type=str, metavar='path', help='output file', required=True)
    csv2bed.add_argument('-o', '--output', type=str, metavar='path', help='input file', required=True)


def action(args):
    load_alignments.export_to_bed(args.input,
                                    args.output)
