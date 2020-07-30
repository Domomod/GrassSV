import subprocess

TEXT = 'pipeline_runner'

MUTATION = ''  # TODO: path to script
ART = ''
INDEX = ''
BOWTIE = ''
SORT = ''
DEPTH = ''
CON_DEPTH = ''
FASTQ = ''
GRASSHOPPER = ''
QUAST = ''


def add_subparser(subparsers):
    pipeline_runner = subparsers.add_parser(TEXT, help='')
    pipeline_runner.add_argument('-o', '--output', type=str, metavar='path', help='output folder', required=True)
    # pipeline_runner.add_argument()    # TODO: input
    pipeline_runner.add_argument('-d', '--depth', type=str, help='Depth coverage', required=False)


def action(args):
    path = args.output
    process_run(MUTATION, path)
    process_run(ART, path)
    process_run(INDEX, path)
    process_run(BOWTIE, path)
    process_run(SORT, path)
    process_run(DEPTH, path)
    process_run(CON_DEPTH, path)  # TODO: not rly like that   # TODO: args.depth
    process_run(FASTQ, path)  # TODO: not rly like that
    process_run(GRASSHOPPER, path)  # TODO: solve gpu problem
    process_run(QUAST, path)


def process_run(*args):
    process = subprocess.run(list(args), stdout=subprocess.PIPE, universal_newlines=True)
    print(process.stdout)
