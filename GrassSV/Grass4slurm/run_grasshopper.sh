#!/bin/bash
#SBATCH -ptesla
#SBATCH --gres=gpu:2
#SBATCH --job-name=grasshopper
#SBATCH -o grasshopper-slurm.out
#SBATCH -e grasshopper-slurm.err
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=ksychla5@gmail.com

module load gcc/7.4.0
module load plgrid/apps/bowtie/1.0.0
module load plgrid/apps/bowtie2/2.2.3
module load plgrid/tools/samtools/1.6.0
module load cuda/10.0.130_410.48

TRIMMOMATIC_PATH=/home/plgrid-groups/plggillumina/plgDominikKrzysztofJulia/tools/Trimmomatic-0.39

coverage_dir=$1
grasshopper_name=$2
grasshopper_dir=$coverage_dir/$grasshopper_name

printf "[+] Grasshopper ("$grasshopper_dir"):\t"
mkdir $grasshopper_dir

grasshopper preprocess $coverage_dir/filtered_reads_C1.fastq $coverage_dir/filtered_reads_C2.fastq -ds=$grasshopper_dir -trimpath=$TRIMMOMATIC_PATH -trimparams="SLIDINGWINDOW:8:15 LEADING:5 TRAILING:5 MINLEN:30"
grasshopper build $grasshopper_dir -ps=33
grasshopper traverse $grasshopper_dir
grasshopper correct $grasshopper_dir
printf "Done\n"