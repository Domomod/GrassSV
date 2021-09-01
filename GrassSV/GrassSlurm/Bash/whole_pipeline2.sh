#!/bin/bash
#SBATCH -ptesla
#SBATCH --gres=gpu:2
#SBATCH --job-name=GrassSV
#SBATCH -o grassSV.log
#SBATCH -e grassSV.log
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=dwitczak@gmail.com

data=${1:=.}         
for coverage in 5 7 10 12
do
	for margin in 150 #250 350 450
	do
		run_grasshopper.sh ${data}/coverage_${coverage}_${margin} grasshopper
	done
done

