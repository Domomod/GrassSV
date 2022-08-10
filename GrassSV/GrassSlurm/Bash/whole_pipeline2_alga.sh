#!/bin/bash
#SBATCH -ptesla
#SBATCH --gres=gpu:2
#SBATCH --job-name=GrassSV
#SBATCH -o grassSV.log
#SBATCH -e grassSV.log
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=dwitczak@gmail.com
#SBATCH --mem=20G

data=${1:=.}         
for coverage in 5 7 10 12
do
	for margin in 150 #250 350 450
	do
		/usr/bin/time -o ${data}/coverage_${coverage}_${margin}/log/run_alga.txt -v run_alga.sh ${data}/coverage_${coverage}_${margin}
	done
done

