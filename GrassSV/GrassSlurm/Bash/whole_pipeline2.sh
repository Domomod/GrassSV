#!/bin/bash
#SBATCH -ptesla
#SBATCH --gres=gpu:2
#SBATCH --job-name=GrassSV
#SBATCH -o grassSV.log
#SBATCH -e grassSV.log
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=dwitczak@gmail.com
#SBATCH --mem=20G

module load gcc/7.4.0
module load bowtie/1.0.0
module load bowtie2/2.2.3
module load samtools/1.6.0
module load cuda/10.0.130_410.48
module load java8/jdk1.8.0_40

data=${1:=.}         
for coverage in 5 7 10 12
do
	for margin in 150 #250 350 450
	do
		/usr/bin/time -o ${data}/coverage_${coverage}_${margin}/log/run_grasshopper.time -v run_grasshopper.sh ${data}/coverage_${coverage}_${margin} grasshopper 
        done
done

