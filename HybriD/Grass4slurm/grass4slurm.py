#!/usr/bin/python3
import argparse
import os.path
import subprocess

class Grass4slurm:
    mail = None
    coverage = None
    margin = None
    reads = None
    calculate_depth = None
    extract_reads = None
    assemble = None
    map_contigs = None
    detect = None

    @staticmethod
    def run():
        # create the top-level parser
        Grass4slurm.create_interface()
        Grass4slurm.check_pipeline_logic()
        Grass4slurm.check_file_existance()
        Grass4slurm.submit_jobs()



    @staticmethod
    def create_interface():
        parser = argparse.ArgumentParser(prog='Grass4slurm')
        parser.add_argument('--mail', type=str,
                            help="Specify you email to get notification when job completes")
        parser.add_argument('--coverage', type=int, nargs='+', default='5',
                            help="Maximum coverage of extracted reads")
        parser.add_argument('--margin', type=int, nargs='+', default='150',
                            help="Maximum coverage of extracted reads")
        parser.add_argument('--reads', type=str, nargs=2, default=['reads1.fq', 'reads2.fq'],
                            help="")
        parser.add_argument('--calculate_depth', action='store_true',
                            help="Extracts reads for assembly process. Use --reads option for non default input file names.")
        parser.add_argument('--extract_reads', action='store_true',
                            help="Extracts reads for assembly process. Use --reads option for non default input file names.")
        parser.add_argument('--assemble', action='store_true',
                            help="Assembles extracted reads into contigs, and maps them using grasshopper and quast")
        parser.add_argument('--map_contigs', action='store_true',
                            help="Enable extract_reads step as part of your pipeline")
        parser.add_argument('--detect', action='store_true',
                            help="Enable extract_reads step as part of your pipeline")

        args = parser.parse_args()

        Grass4slurm.mail            = args.mail
        Grass4slurm.coverage        = args.coverage if isinstance(args.coverage, list) else [args.coverage]
        Grass4slurm.margin          = args.margin if isinstance(args.margin, list) else [args.margin]
        Grass4slurm.reads           = args.reads
        Grass4slurm.calculate_depth = args.calculate_depth
        Grass4slurm.extract_reads   = args.extract_reads
        Grass4slurm.assemble        = args.assemble
        Grass4slurm.map_contigs     = args.map_contigs
        Grass4slurm.detect          = args.detect

    @staticmethod
    def check_pipeline_logic():

        pass

    @staticmethod
    def check_file_existance():
        def check_file(file):
            if not os.path.isfile(file):
                print(f"File {file} does not exist.")
                exit(-1)
        def check_dir(dir):
            if not os.path.isdir(dir):
                print(f"Directory {dir} does not exist.")
                exit(-1)

        for coverage in Grass4slurm.coverage:
            for margin in Grass4slurm.margin:
                directory=f"coverage_{coverage}_{margin}"
                if Grass4slurm.extract_reads is False:
                    check_dir(directory)

                if Grass4slurm.extract_reads is True or Grass4slurm.calculate_depth is True:
                    file = f"{Grass4slurm.reads[0]}"
                    check_file(file)

                    file = f"{Grass4slurm.reads[1]}"
                    check_file(file)


                if Grass4slurm.assemble is True and Grass4slurm.extract_reads is False:
                    check_dir(directory)
                    file = f"{directory}/filtered_reads_C1.fastq"
                    check_file(file)
                    file = f"{directory}/filtered_reads_C2.fastq"
                    check_file(file)

                if Grass4slurm.map_contigs is True and Grass4slurm.assemble is False:
                    check_dir(directory)
                    check_dir(f"{directory}/grasshopper")
                    check_file(f"{directory}/grasshopper/contigs.fasta")

                if Grass4slurm.detect is True and Grass4slurm.map_contigs is False:
                    check_dir(directory)
                    check_dir(f"{directory}/grasshopper")
                    check_file(f"{directory}/grasshopper/quast/contigs_reports/all_alignments_contigs.tsv")

        pass

    @staticmethod
    def submit_jobs():
        for coverage in Grass4slurm.coverage:
            for margin in Grass4slurm.margin:
                reads = Grass4slurm.reads
                coverage_folder = f"coverage_{coverage}_{margin}"
                depend = -1

                def submit_job(cmd):
                    output = subprocess.getoutput(cmd)
                    depend = output.split(' ')[-1].strip()

                if Grass4slurm.calculate_depth == True:
                    cmd = 'sbatch' \
                             + f' --depend=afterok:{depend} --kill-on-invalid-dep=yes' if depend!= -1 else ''\
                             + f' --mail-type=END,FAIL --mail-user={Grass4slurm.mail}' if Grass4slurm.mail is not None else ''\
                             + f' HybriD/Grass4slurm/calculate_depth.sh .'

                if Grass4slurm.extract_reads == True:
                    cmd = 'sbatch' \
                             + f' --depend=afterany:{depend} ' if depend!= -1 else ''\
                             + f' --mail-type=END,FAIL --mail-user={Grass4slurm.mail}' if Grass4slurm.mail is not None else ''\
                             + f' HybriD/Grass4slurm/extract_reads.sh . {coverage} {margin}'

                if Grass4slurm.assemble == True:
                    cmd = 'sbatch' \
                             + f' --depend=afterany:{depend} ' if depend!= -1 else ''\
                             + f' --mail-type=END,FAIL --mail-user={Grass4slurm.mail}' if Grass4slurm.mail is not None else ''\
                             + f' HybriD/Grass4slurm/run_grasshopper.sh ./{coverage_folder} grasshopper'

                if Grass4slurm.map_contigs == True:
                    cmd = 'sbatch' \
                             + f' --depend=afterany:{depend} ' if depend!= -1 else ''\
                             + f' --mail-type=END,FAIL --mail-user={Grass4slurm.mail}' if Grass4slurm.mail is not None else ''\
                             + f' HybriD/Grass4slurm/run_quast.sh ./{coverage_folder} quast'

                if Grass4slurm.detect == True:
                    cmd = 'sbatch' \
                             + f' --depend=afterany:{depend} ' if depend!= -1 else ''\
                             + f' --mail-type=END,FAIL --mail-user={Grass4slurm.mail}' if Grass4slurm.mail is not None else ''\
                             + f' HybriD/Grass4slurm/extract_reads.sh . {coverage} {margin}'

Grass4slurm.run()