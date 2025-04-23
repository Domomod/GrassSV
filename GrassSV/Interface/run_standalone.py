import argparse#, argcomplete
from GrassSV.GrassDocker import run_standalone
from enum import Enum, IntEnum

TEXT = 'run_standalone'

def add_subparser(subparsers):
    slurm_dispatch = subparsers.add_parser(TEXT, help='Runs GrassSV pipeline in a single run')
    slurm_dispatch.add_argument('-g', '--genome', type=str, metavar='path', help='Path to genome (fasta format).', required=True)
    slurm_dispatch.add_argument('-i', '--index', type=str, metavar='path',  help='Path to genome_lengths', required=True)
    slurm_dispatch.add_argument('-l', '--length', type=str, metavar='path', help='Path to genome index', required=True)
    slurm_dispatch.add_argument('-r', '--reads1', type=str, metavar='path', help='Path to reads1 (fastq format)', required=True)
    slurm_dispatch.add_argument('-R', '--reads2', type=str, metavar='path', help='Path to reads2 (fastq format)', required=True)


def action(args):
    run_standalone.run_standalone(args.genome, args.length, args.index, args.reads1, args.reads2)
