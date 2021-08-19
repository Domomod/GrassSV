#!/bin/bash
#SBATCH -pfast 
#SBATCH --job-name=alga
#SBATCH -o alga-slurm.out
#SBATCH -e alga-slurm.err
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=domionato@gmail.com

module load gcc/7.4.0
module load bowtie/1.0.0
module load bowtie2/2.2.3
module load samtools/1.6.0

dir=$1

printf "[+] Alga ("alga"):\t"
mkdir -p alga

ALGA --file1=${dir}/filtered_reads_C1.fastq --file2=${dir}/filtered_reads_C2.fastq --threads=8 --output=${dir}/alga/contigs.fasta

printf "Alga ended with code $?\n"
