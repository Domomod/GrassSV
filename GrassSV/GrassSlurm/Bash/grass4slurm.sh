#!/bin/bash

#SBATCH -J grass4slurm
#SBATCH -e log/grass4slurm.err
#SBATCH -o log/grass4slurm.out 

module load python/3.7.3

Grass4slurm --all
