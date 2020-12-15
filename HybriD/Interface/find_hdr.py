from HybriD.Scripts import find_hdr

TEXT = 'find_hdr'


def add_subparser(subparsers):
    hdr = subparsers.add_parser(TEXT, help='finds regions of intrest based on mapping coverage')
    hdr.add_argument('input', type=str)
    hdr.add_argument('output', type=str)  # TODO: dodaj inne parametry


def action(args):
    find_hdr.find_hdr(args.input, args.output)
