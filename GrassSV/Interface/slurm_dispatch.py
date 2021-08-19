from GrassSV.GrassSlurm import slurm_scheduler
TEXT = 'slurm_dispatch'

def add_subparser(subparsers):
    slurm_dispatch = subparsers.add_parser(TEXT, help='')
    slurm_dispatch.add_argument('-o', '--output', type=str, metavar='path', help='output folder', required=True)
    # pipeline_runner.add_argument()    # TODO: input
    slurm_dispatch.add_argument('-d', '--depth', type=str, help='Depth coverage', required=False)


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
