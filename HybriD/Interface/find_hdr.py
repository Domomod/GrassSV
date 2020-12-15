from HybriD.Scripts import find_hdr

TEXT = 'find_hdr'


def add_subparser(subparsers):
    hdr = subparsers.add_parser(TEXT, help='finds regions of high depth coverage')
    hdr.add_argument('input', type=str)
    hdr.add_argument('output', type=str)
    hdr.add_argument('-w', '--window', help="Window size (default is 70)", default=70, type=int, required=False)
    hdr.add_argument('-th', '--threshold', help="Threshold size (default is None - auto detect)", default=None,
                     type=int, required=False)
    hdr.add_argument('-m', '--min_consecutive_region', help="Minimal consecutive region to detect (default is 1000)",
                     default=1000, type=int, required=False)


def action(args):
    find_hdr.find_hdr(args.input, args.output, args.window, args.threshold, args.min_consecutive_region)
