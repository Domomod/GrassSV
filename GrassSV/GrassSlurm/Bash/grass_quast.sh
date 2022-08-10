#!/bin/bash
#SBATCH -ptesla
#SBATCH --gres=gpu:2
#SBATCH --job-name=grasshopper
#SBATCH -o grasshopper-slurm.out
#SBATCH -e grasshopper-slurm.err
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=ksychla5@gmail.com
#SBATCH --mem=20G

run_grasshopper.sh . grasshopper
run_quast.sh ./grasshopper quast

