import argparse
from HybriD.Alignment import  run

TEXT = 'find_sv'


def add_subparser(subparsers):
    find_sv = subparsers.add_parser(TEXT, help='finds structural variations based on contig\'s mappings')
    find_sv.add_argument('alignments', type=str)
    find_sv.add_argument('-o','--output', type=str, metavar='path', help="output folder", required=True)
    #TODO: implement csv output
    find_sv.add_argument('-b','--format', type=str, choices = ['bed', 'csv'], help="saves findings in bed format")
    find_sv.add_argument('-s','--save_svs', action='store_true', help="saves findings in bed format")
    find_sv.add_argument('-p','--save_patterns', action='store_true', help="saves findings in bed format")
    find_sv.add_argument('-a','--save_supporting_alignments', action='store_true', help="saves findings in bed format")
    #TODO: implement validation
    find_sv.add_argument('--validate', type=str, metavar="path.csv", nargs='+',
                         help="validates findings against supplied mutations")


def action(args):
    run.run(args.alignments,
            export_patterns=args.save_patterns,
            export_supporting_alignments=args.save_supporting_alignments,
            output_folder_path=args.output)
    pass
