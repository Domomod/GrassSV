import argparse, argcomplete
from GrassSV.GrassSlurm import slurm_scheduler
from enum import Enum




TEXT = 'slurm_dispatch'

def add_subparser(subparsers):
    slurm_dispatch = subparsers.add_parser(TEXT, help='')
    slurm_dispatch.add_argument('-G', '--genMutations', type=str, default="NONE",
                                help="[Optional] You may generate mutations using our fastaDNA generator. To do so specify what mutations do you want to generate: [" + ", ".join([enum.name.lower() for enum in GenMutEnums]) + "]",
                                choices=[enum.name.lower() for enum in slurm_scheduler.GenMutEnums], required=False)

    slurm_dispatch.add_argument('-g', '--genome', type=str, metavar='path', help='The genome file that will be copied to output folder.', required=True)
    slurm_dispatch.add_argument('-o', '--output', type=str, metavar='path', help='The output folder where GrassSv output will be generated. Do not store multiple outputs in the same folder as they would overwrite eachother.', required=True)


def action(args):
    slurm_scheduler.Scheduler.schedule_tasks(args.output, args.genMutations)