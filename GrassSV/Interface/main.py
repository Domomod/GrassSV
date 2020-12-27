import argparse
from GrassSV.Interface import rsvsim2bed, find_sv, find_roi, roi_statistics, quast2bed, filter_reads, pipeline_runner, \
    find_hdr


def run():
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='GrassSV.py')
    subparsers = parser.add_subparsers(help='GrassSV consits of multiple scripts:', dest='action')

    rsvsim2bed.add_subparser(subparsers)
    find_sv.add_subparser(subparsers)
    find_roi.add_subparser(subparsers)
    roi_statistics.add_subparser(subparsers)
    quast2bed.add_subparser(subparsers)
    filter_reads.add_subparser(subparsers)
    pipeline_runner.add_subparser(subparsers)
    find_hdr.add_subparser(subparsers)

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
    elif args.action == pipeline_runner.TEXT:
        pipeline_runner.action(args)
    elif args.action == find_hdr.TEXT:
        find_hdr.action(args)
