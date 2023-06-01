#!/bin/bash

module load samtools/1.6.0
module load bowtie2/2.2.3

#printf "[+] Index :\t"
#bowtie2-build ${genome} ${index}
printf "Done\n[+] Bowtie :\t"
bowtie2 -x ${index} -1 ${reads1} -2 ${reads2} -S ${alignments_file}
printf "Done\n[+] Sort :\t"
samtools sort -o ${alignments_sorted} ${alignments_file}
printf "Done\n[+] Depth :\t"
samtools depth -a ${alignments_sorted} > ${coverage_file}
printf "Done\n"