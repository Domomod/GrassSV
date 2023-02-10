#!/bin/bash
#SBATCH -J quast
#SBATCH -o log/quast.out
#SBATCH -e log/quast.err
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=ksychla5@gmail.com

#quast=/home/wojtek/tools/quast-5.0.2/quast.py
#quast=/home/plgrid-groups/plggillumina/plgDominikKrzysztofJulia/tools/quast-5.0.2/quast.py
quast=quast.py

mkdir -p ${quast_out}
#poprzednio -m 200 -i 65
$quast ${contigs} -r ${genome} -m 250 -o ${quast_out}
printf "Done\n"
