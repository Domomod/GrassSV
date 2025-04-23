import argparse#, argcomplete
import traceback
from GrassSV.Interface import rsvsim2bed, find_sv, find_roi, roi_statistics, quast2bed, filter_reads, slurm_dispatch, find_hdr, run_standalone, utils


def run():
    try:
        # create the top-level parser
        parser = argparse.ArgumentParser(prog='GrassSV.py',
                                        formatter_class=argparse.RawTextHelpFormatter)
        subparsers = parser.add_subparsers(help='GrassSV consits of multiple scripts:', dest='action')

        rsvsim2bed.add_subparser(subparsers)
        find_sv.add_subparser(subparsers)
        find_roi.add_subparser(subparsers)
        roi_statistics.add_subparser(subparsers)
        quast2bed.add_subparser(subparsers)
        filter_reads.add_subparser(subparsers)
        slurm_dispatch.add_subparser(subparsers)
        find_hdr.add_subparser(subparsers)
        run_standalone.add_subparser(subparsers)
        utils.add_subparser(subparsers)

        #argcomplete.autocomplete(parser)
        args = parser.parse_args()

        if args.action == find_sv.TEXT:
            find_sv.action(args)
        elif args.action == find_roi.TEXT:
            find_roi.action(args)
        elif args.action == rsvsim2bed.TEXT:
            rsvsim2bed.action(args)
        elif args.action == roi_statistics.TEXT:
            roi_statistics.action(args)
        elif args.action == quast2bed.TEXT:
            quast2bed.action(args)
        elif args.action == filter_reads.TEXT:
            filter_reads.action(args)
        elif args.action == slurm_dispatch.TEXT:
            slurm_dispatch.action(args)
        elif args.action == find_hdr.TEXT:
            find_hdr.action(args)
        elif args.action == run_standalone.TEXT:
            run_standalone.action(args)    
        elif args.action == utils.TEXT:
            utils.action(args)

    except Exception as e:
        print( '\033[1;31m' ) 
        print( str(e) )
        print( '\033[0;31m' ) 
        print( traceback.format_exc() )
        print( '\033[0m' )
