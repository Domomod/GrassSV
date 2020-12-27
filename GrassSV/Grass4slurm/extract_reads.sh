#!/bin/bash

#SBATCH -J ART
#SBATCH -e log/EXTRACT-slurm.err
#SBATCH -o log/EXTRACT-slurm.out

module load python/3.7.3

mutation_dir=$1
max_depth=$2
margin=$3
coverage_dir=$mutation_dir/coverage_${max_depth}_$margin

mkdir -p $coverage_dir
printf "[+] find_roi ("$mutation_dir"):\t"
HybriD.py find_roi $mutation_dir/depth.coverage $coverage_dir/regions_of_interest.bed $max_depth 1  $margin
printf "Done\n[+] fastq_regions ("$mutation_dir"):\t"
extract_reads.exe $mutation_dir/alignments.sam $coverage_dir/regions_of_interest.bed $coverage_dir/filtered_reads_C1.fastq $coverage_dir/filtered_reads_C2.fastq $coverage_dir 
#GrassSV.py fastq_regions -f1 $coverage_dir/filtered_reads_C1.fastq -f2 $coverage_dir/filtered_reads_C2.fastq -s $mutation_dir/alignments.sam -d $coverage_dir/regions_of_interest.bed:
printf "Done\n"

