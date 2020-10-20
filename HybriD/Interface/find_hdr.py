from HybriD.Scripts import find_hdr

TEXT = 'find_hdr'


def add_subparser(subparsers):
    csv2bed = subparsers.add_parser(TEXT)


def action(args):
    find_hdr.find_hdr()
