#!/bin/bash

#SBATCH --job-name=GrassSV
#SBATCH -o grassSV.log
#SBATCH -e grassSV.log
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=domionato@gmail.com
#SBATCH --mem=20G

data=${1:=.}
for coverage in 5 7 10 12
do
	for margin in 150 #250 350 450
	do
		extract_reads.sh $data $coverage $margin
	done
done

