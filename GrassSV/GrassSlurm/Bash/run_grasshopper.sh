#!/bin/bash
#SBATCH -ptesla
#SBATCH --gres=gpu:2
#SBATCH --job-name=grasshopper
#SBATCH -o grasshopper-slurm.out
#SBATCH -e grasshopper-slurm.err
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=ksychla5@gmail.com

module load gcc/7.4.0
module load bowtie/1.0.0
module load bowtie2/2.2.3
module load samtools/1.6.0
module load cuda/10.0.130_410.48

if [[ -z $TRIMMOMATIC_PATH ]]
then
  echo "[WARNING] TRIMMOMATIC_PATH not set, falling back to default value" > 2
  TRIMMOMATIC_PATH=/home/tools/Trimmomatic-0.39
fi

coverage_dir=$1
grasshopper_name=$2
grasshopper_dir=$coverage_dir/$grasshopper_name

printf "[+] Grasshopper ("$grasshopper_dir"):\t"
mkdir -p $grasshopper_dir

grasshopper preprocess $coverage_dir/filtered_reads_C1.fastq $coverage_dir/filtered_reads_C2.fastq -ds=$grasshopper_dir -trimpath=$TRIMMOMATIC_PATH -trimparams="SLIDINGWINDOW:8:15 LEADING:5 TRAILING:5 MINLEN:30 CROP:120"
grasshopper build $grasshopper_dir -ps=33
grasshopper traverse $grasshopper_dir
grasshopper correct $grasshopper_dir
printf "Done\n"
