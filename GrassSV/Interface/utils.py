import argparse, argcomplete, textwrap

from GrassSV.Scripts import csv2bed, check_sv

TEXT = 'utils'

CSV2BED = "csv2bed"
CHECK_SV = "check_sv"


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
    check_sv.add_argument('-d', '--detected', type=str, metavar='path', help='Path to direcotry containing detected mutations', required=True)

def action(args):
    if args.utils_action == CSV2BED:
        csv2bed.export_to_bed(input_path= args.vcf, output_path = args.bed)
        pass
    elif args.utils_action == CHECK_SV:
        check_sv.check_sv(detected_dir = args.detected, generated_dir = args.generated )
        pass
