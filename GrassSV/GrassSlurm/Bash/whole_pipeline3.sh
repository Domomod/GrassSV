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
alignments=${4:-quast/contigs_reports/all_alignments_contigs.tsv}        

/usr/bin/time -v GrassSV.py find_hdr ${data}/depth.coverage ${data}/duplications.bed.temp 2> find_hdr.txt
for coverage in 5 7 10 12
do
	for margin in 150 #250 350 450
	do
		/usr/bin/time -v run_quast.sh ${data}/coverage_${coverage}_${margin}/${assembler}/${contigs} quast 2> run_qast_${coverage}_${margin}.txt
		/usr/bin/time -v GrassSV.py find_sv ${data}/coverage_${coverage}_${margin}/${assembler}/${alignments} -o ${data}/coverage_${coverage}_${margin}/${assembler}/ 2> find_sv_${coverage}_${margin}.txt
		cp ${data}/duplications.bed.temp  ${data}/coverage_${coverage}_${margin}/${assembler}/detectedSVs/duplications.bed
	done
done
rm ${data}/duplications.bed.temp
