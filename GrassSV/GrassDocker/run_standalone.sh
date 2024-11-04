#!/bin/bash 

Help()
{
   # Display Help
   echo "This will run all steps for GrassSV pipeline in a single process."
   echo
   echo "Syntax: $0 [-g|l|i|r|R|h]"
   echo "options:"
   echo "g     Path to genome (fasta format)"
   echo "l     Path to genome_lengths"
   echo "i     Path to genome index"
   echo "r     Path to reads1 (fastq format)"
   echo "R     Path to reads2 (fastq format)"
   echo "h     Show this helpe message"
   echo
}

while getopts 'g:l:i:r:R:h' OPTION; do
  case "$OPTION" in
    
    g)
      echo "Genome file: \"$OPTARG\""
      genome=$OPTARG
      ;;
    l)
      echo "Genome length file: \"$OPTARG\""
      genome_lengths=$OPTARG
      ;;
    i)
      echo "Genome index file: \"$OPTARG\""
      index=$OPTARG
      ;;
    r)
      echo "Reads 1 file: \"$OPTARG\""
      reads1=$OPTARG
      ;;
    R)
      echo "Reads 2 file: \"$OPTARG\""
      reads2=$OPTARG
      ;;   
    h)
      Help
	  exit 0
      ;;
    ?)
      Help
      exit 1
      ;;
  esac
done

#Input: coverage margin 
#For GMP server
#: "${work_dir:=out_${GMPTOOLS_USER}_${GMPTOOLS_JOB}}"; export work_dir
: "${work_dir:=.}"                                ; export work_dir
: "${coverage:=10}"                                  ; export coverage
: "${margin:=150}"                                   ; export margin
: ${genome}                                          ; export genome
: ${genome_lengths}                                  ; export genome_lengths
: ${index}                                           ; export index
: ${reads1}                                          ; export reads1
: ${reads2}                                          ; export reads2


#Can be overwritten by variables exported by the caller
: ${alignments_file:=${work_dir}/alignments.sam}          ; export alignments_file
: ${alignments_sorted:=${work_dir}/alignments_sorted.sam} ; export alignments_sorted
: ${coverage_file:=${work_dir}/depth.coverage}            ; export coverage_file

free -h
echo "Coverage: ${coverage}"
echo "Margin: ${margin}"

export roi=${work_dir}/regions_of_interest.bed
export filtered_reads1=${work_dir}/filtered_reads_C1.fastq
export filtered_reads2=${work_dir}/filtered_reads_C2.fastq
#export contigs=${work_dir}/alga/contigs.fasta
export contigs=${work_dir}/alga/contigs.fasta_contigs.fasta
export quast_out=${work_dir}/quast
#export quast_alignments=${quast_out}/contigs_reports/all_alignments_contigs.fasta_c.tsv
export quast_alignments=${quast_out}/contigs_reports/all_alignments_contigs-fasta_contigs.tsv

export results=${work_dir}/results

mkdir -p $work_dir
mkdir -p $(dirname ${contigs})
mkdir -p quast_out

printf "Input parameters coverage: ${coverage}margin: ${margin}" > ${work_dir}/README.txt 
env > ${work_dir}/env.txt

#Use bash tasks relative to run_standalone.sh
scriptDir=$(dirname -- "$(readlink -f -- "$BASH_SOURCE")")/Bash

# Comment out when not using SLURM
module load python/3.9.2
echo $PATH > path.txt

echo "[+] calculate_depth:"
$scriptDir/calculate_depth.sh
echo "[+] find_roi:"
GrassSV.py find_roi ${coverage_file} ${roi} ${coverage} -m ${margin} > ${work_dir}/find_roi.txt
echo "[+] fastq_regions:"
GrassSV.py filter_reads -f1 ${filtered_reads1} -f2 ${filtered_reads2} -s ${alignments_file} -ss ${alignments_sorted} -roi ${roi} > ${work_dir}/filter_reads.txt
echo "[+] Alga:"
$scriptDir/run_alga.sh > ${work_dir}/run_alga.txt
echo "[+] Quast:"
$scriptDir/run_quast.sh > ${work_dir}/run_quast.txt
echo "[+] find_sv:"
GrassSV.py find_sv ${quast_alignments} -o ${results} > ${work_dir}/find_sv.txt
echo "[+] find_hdr:"
GrassSV.py find_hdr ${coverage_file} ${results}/duplications.bed  > ${work_dir}/find_hdr.txt
