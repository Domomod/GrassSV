#!/bin/bash

#SBATCH --job-name=GrassSV
#SBATCH -o grassSV.log
#SBATCH -e grassSV.log
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=domionato@gmail.com

module load python/3.7.3

data=${1:-.}
assembler=${2:-grasshopper}
contigs=${3:-contigs.fsa}
alignments=${3:-quast/contigs_reports/all_alignments_contigs.tsv}        

for coverage in 5 7 10 12
do
	for margin in 150 #250 350 450
	do
		run_quast.sh ${data}/coverage_${coverage}_${margin}/${assembler}/${contigs} quast
		GrassSV.py find_sv ${data}/coverage_${coverage}_${margin}/${assembler}/${alignments} -o ${data}/coverage_${coverage}_${margin}/${assembler}/
	done
done

