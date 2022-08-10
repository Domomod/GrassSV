#!/bin/bash

#SBATCH --job-name=GrassSV
#SBATCH -o grassSV.log
#SBATCH -e grassSV.log
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=domionato@gmail.com
#SBATCH --mem=20G

module load python/3.7.3

work_dir=${1:-.}
assembler=${2:-grasshopper}
contigs=${3:-contigs.fsa}

${4:-quast/contigs_reports/all_alignments_contigs.tsv}        

/usr/bin/time -v GrassSV.py find_hdr ${work_dir}/depth.coverage ${work_dir}/duplications.bed.temp 2> find_hdr.txt
for coverage in 5 7 10 12
do
	for margin in 150 #250 350 450
	do
		coverage_dir=${work_dir}/coverage_${coverage}_${margin}
		assembler_dir=${coverage_dir}/${assembler}
		alignments_dir=${assembler_dir}/quast/contigs_reports
		alignments=$(find ${alignments_dir} -name "all_alignments_*" -print -quit) 
		echo Alignments path: ${alignments}

		/usr/bin/time -o ${coverage_dir}/log/run_quast.time -v run_quast.sh ${assembler_dir}/${contigs} quast
		/usr/bin/time -o ${coverage_dir}/log/find_sv.time  -v GrassSV.py find_sv ${alignments} -o ${assembler_dir}/
		cp ${work_dir}/duplications.bed.temp  ${assembler_dir}/detectedSVs/duplications.bed
	done
done
rm ${work_dir}/duplications.bed.temp
