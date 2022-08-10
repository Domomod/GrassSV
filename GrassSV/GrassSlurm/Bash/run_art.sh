#!/bin/bash

#SBATCH -J ART
#SBATCH -e log/ART-slurm.err
#SBATCH -o log/ART-slurm.out
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=domionato@gmail.com
#SBATCH --mem=20G

data=$1

printf "[+] ART ("$data"):\t"
art_illumina -ss HS25 -i $data/genome.fsa -p -l 75 -f 20 -m 500 -s 50 -o $data/reads
printf "Done\n"
