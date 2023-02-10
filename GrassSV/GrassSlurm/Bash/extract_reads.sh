#!/bin/bash

#SBATCH -J ART
#SBATCH -e log/EXTRACT-slurm.err
#SBATCH -o log/EXTRACT-slurm.out
#SBATCH --mem=100G

module load python/3.9.2

mutation_dir=$1
max_depth=$2
margin=$3
coverage_dir=$mutation_dir/coverage_${max_depth}_$margin

mkdir -p $coverage_dir
mkdir -p ${coverage_dir}/log
printf "[+] find_roi ("$mutation_dir"):\t"
printf "Calling: GrassSV.py find_roi "$mutation_dir"/depth.coverage "$coverage_dir"/regions_of_interest.bed "$max_depth" -m "$margin"\n"a
/usr/bin/time -v -o ${coverage_dir}/log/find_roi.txt \
  GrassSV.py find_roi $mutation_dir/depth.coverage $coverage_dir/regions_of_interest.bed $max_depth -m $margin 
printf "Done\n[+] fastq_regions ("$mutation_dir"):\t"
#extract_reads.exe $mutation_dir/alignments.sam $coverage_dir/regions_of_interest.bed $coverage_dir/filtered_reads_C1.fastq $coverage_dir/filtered_reads_C2.fastq $coverage_dir 
/usr/bin/time -v -o ${coverage_dir}/log/filter_reads.txt \
  GrassSV.py filter_reads -f1 $coverage_dir/filtered_reads_C1.fastq -f2 $coverage_dir/filtered_reads_C2.fastq -s $mutation_dir/alignments.sam -ss $mutation_dir/alignments_sorted.sam -roi $coverage_dir/regions_of_interest.bed
printf "Done\n"

