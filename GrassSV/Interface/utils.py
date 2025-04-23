import argparse, textwrap#, argcomplete

from GrassSV.Scripts import csv2bed, check_sv, check_breakpoint

TEXT = 'utils'

CSV2BED = "csv2bed"
CHECK_SV = "check_sv"
CHECH_SV_BR = "check_sv_br"

def add_subparser(subparsers):
    utils = subparsers.add_parser(TEXT, help='Utilities [csv2bed, sv_check]',
                                    description="\033[1;36m" 
                                                "Convert alignments produced by quast from tsv format to bed, for later visualization" 
                                                "\033[0m",
                                    formatter_class=argparse.RawTextHelpFormatter)
                                    
    utils_subparer = utils.add_subparsers(help='GrassSV utils consits of multiple scripts:', dest='utils_action')


    csv2bed = utils_subparer.add_parser(CSV2BED, 
                                        help="Convert csv sequences to bed",
                                        description="Vcf2bed converts 1-based, closed [start, end] Variant Call Format v4.2 (VCF) to 0-based, half-open [start-1, end) extended BED data.")
    csv2bed.add_argument('-i', '--vcf', type=str, metavar='path', help='Input file (vcf format)', required=True)
    csv2bed.add_argument('-o', '--bed', type=str, metavar='path', help='Output file (bed format)', required=True)

    check_sv = utils_subparer.add_parser(CHECK_SV, 
                                        formatter_class=argparse.RawTextHelpFormatter,
                                        help="Compare two files with structural variations",
                                        description="\033[1;36m"
                                                    "Checks how many sv from [-d] input files can be also found in [-g] input files.\n"
                                                    "Both [-t] and [-g] need to point to directories of following format:\n"
                                                    "directory/:\n"
                                                    "   deletions.bed\n" 
                                                    "   duplications.bed\n" 
                                                    "   inversions.bed.bed\n" 
                                                    "   insertion.bed\n" 
                                                    "   translocations.bed\n"
                                                    "\033[0m")
    check_sv.add_argument('-g', '--generated', type=str, metavar='path', help='Path to directory containing generated/known mutations', required=True)
    check_sv.add_argument('-d', '--detected', type=str, metavar='path', help='Path to directory containing detected mutations', required=True)
    check_sv.add_argument('-b', '--bp_mode', help='Alternative mode: Loads only breakpoints.bed from direcotry/', action='store_true')

    check_sv_br = utils_subparer.add_parser(CHECH_SV_BR, 
                                        formatter_class=argparse.RawTextHelpFormatter,
                                        help="Compare two files with structural variations in breakpoint format",
                                        description="\033[1;36m"
                                                    "Checks how many breakpoints from [-g] input files can be also found in [-d] input files.\n"
                                                    "The generated breakpoints may be manualy enlarged on both sizes, to allow for a margin of error. \n"
                                                    "\033[0m")
    check_sv_br.add_argument('-g', '--generated', type=str, metavar='path', help='Path to directory containing generated/known mutations', required=True)
    check_sv_br.add_argument('-d', '--detected', type=str, metavar='path', help='Path to direcotry containing detected mutations', required=True)


def action(args):
    if args.utils_action == CSV2BED:
        csv2bed.export_to_bed(input_path= args.vcf, output_path = args.bed)
        pass
    elif args.utils_action == CHECK_SV:
        check_sv.check_sv(detected_dir = args.detected, generated_dir = args.generated, only_breakpoints=args.bp_mode )
        pass
    elif args.utils_action == CHECH_SV_BR:
        check_breakpoint.check_sv(detected_dir = args.detected, generated_dir = args.generated )
        pass
