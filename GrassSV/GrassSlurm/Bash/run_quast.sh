#!/bin/bash
#SBATCH -J quast
#SBATCH -o log/quast.out
#SBATCH -e log/quast.err
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=ksychla5@gmail.com

quast=/home/plgrid-groups/plggillumina/plgDominikKrzysztofJulia/tools/quast-5.0.2

contigs_path=$1
grasshopper_dir=$(dirname $1)
genome_dir=$grasshopper_dir/../../../../genome
quast_name=$2
quast_dir=$grasshopper_dir/$quast_name
mkdir -p $quast_dir



printf "[+] Quast ("$quast_dir"):\t"
#poprzednio -m 200 -i 65
$quast/quast.py $contigs_path -r $genome_dir/ref.fsa -m 250 -o $quast_dir
printf "Done\n"
