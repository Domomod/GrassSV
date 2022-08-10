#!/bin/bash

#SBATCH -n16
#SBATCH -N1
#SBATCH -p standard
#SBATCH -J glebokosc_pokrycia
#SBATCH -o log/depth-slurm.out
#SBATCH -e log/depth-slurm.err

module load samtools/1.6.0
module load bowtie2/2.2.3

main_directory=$1/../..
mutation_dir=$1
genome=$main_directory/genome/ref.fsa 
index_dir=$main_directory/index

printf "[+] Index ("$main_directory"):\t"
/usr/bin/time -o ${mutation_dir}/log/bowtie2_build.time -v bowtie2-build $genome $index_dir/index
printf "Done\n[+] Bowtie ("$main_directory"):\t"
/usr/bin/time -o ${mutation_dir}/log/bowti2.time -v bowtie2 -x $index_dir/index -1 $mutation_dir/reads1.fq -2 $mutation_dir/reads2.fq -S $mutation_dir/alignments.sam
printf "Done\n[+] Sort ("$main_directory"):\t"
/usr/bin/time -o ${mutation_dir}/log/samtools_sort.time -v samtools sort -o $mutation_dir/alignments_sorted.sam $mutation_dir/alignments.sam
printf "Done\n[+] Depth ("$main_directory"):\t"
/usr/bin/time -o ${mutation_dir}/log/samtools_depth.txt -v samtools depth -a $mutation_dir/alignments_sorted.sam > $mutation_dir/depth.coverage
printf "Done\n"
