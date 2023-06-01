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
export contigs=${work_dir}/alga/contigs.fasta
export contigs_with_alga_sufix=${work_dir}/alga/contigs.fasta_contigs.fasta

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
scriptDir=$(dirname "$(which run_standalone.sh)")/Bash/
echo "Current scriptDir: $scriptDir"
# Comment out when not using SLURM
module load python/3.9.2
echo $PATH > path.txt

# Declare an array to store job IDs
declare -a fastq_regions_jobids

# Find roi
# find_roi_cmd=$(cat <<-EOF
#     GrassSV.py find_roi ${coverage_file} ${roi} ${coverage} -m ${margin} > ${work_dir}/find_roi.txt
# EOF
# )

# find_roi_jobid=$(sbatch --time=48:00:00 --mail-type=ALL --mail-user=dominik.piotr.witczak@gmail.com --mem=200GB -n 1 --output=./log/find_roi.out --wrap "$find_roi_cmd" | awk '{print $NF}')

#!/bin/bash

# Function to parse named arguments

parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --job-name=*)
                job_name="${1#*=}"
                shift
                ;;
            --dependency=*)
                dependency="${1#*=}"
                shift
                ;;
            --job_id_out=*)
                job_id_out="${1#*=}"
                shift
                ;;
            --cmd=*)
                command="${1#*=}"
                shift
                ;;
            
        esac
    done
}

# Function to construct the dependency option if provided
construct_dependency_string() {
    local dependency="$1"
    local dependency_option=""

    if [[ -n $dependency ]]; then
        dependency_option="--dependency=$dependency"
    fi

    echo "$dependency_option"
}

# Function to submit Slurm job and return the job ID
submit_job() {
    job_name=""
    dependency=""
    command=""
    job_id_out=""
    parse_arguments "$@"
  
    # echo "Job Name: $job_name"
    # echo "Dependency: $dependency"
    # echo "Command:"
    # echo "$command"
    # echo "Job ID Out: $job_id_out"
    # echo "--------------------------------------"

    # Construct dependency option if provided
    local dependency_option="$(construct_dependency_string "$dependency")"

    # Submit the Slurm job and print the job ID
    local job_id=$(sbatch --job-name="$job_name" --time=48:00:00 --mail-type=ALL --mail-user=dominik.piotr.witczak@gmail.com --mem=200GB --output="$work_dir/$job_name.out" $dependency_option --wrap "$command" | awk '{print $NF}')
    echo "Submitted job ($job_name) with ID: $job_id and dependency on: $dependency"

    # Assign the job ID to the provided variable if requested
    if [[ -n $job_id_out ]]; then
        eval "$job_id_out='$job_id'"
    fi
}

# Define the necessary job ID variables
batch_sort_jobid=""
fastq_regions_jobid=""
fastq_regions_jobids=()
merge_filtered_reads_jobid=""
alga_jobid=""
quast_jobid=""
find_sv_jobid=""
find_hdr_jobid=""

# for read_num in aa ab ac ad ae af ag; do
#     alignments_file="./alignments_${read_num}.sam"
#     sorted_alignments_file="./alignments_sorted_${read_num}.sam"
#     filtered_reads1_file="${work_dir}/filtered_reads1_${read_num}.fastq"
#     filtered_reads2_file="${work_dir}/filtered_reads2_${read_num}.fastq"

#     # module load bowtie2/2.2.3
#     # bowtie2 -x ${index} -1 reads1_part_${read_num}.fq -2 reads2_part_${read_num}.fq -S ${alignments_file}
#     export batch_sort_cmd=$(cat <<-EOF
#         module load samtools/1.6.0
#         rm ${sorted_alignments_file}.tmp*
#         samtools sort -o ${sorted_alignments_file} ${alignments_file}
#         touch ${sorted_alignments_file}
# EOF
#     )

#     submit_job --job-name=batch_sort_${read_num} --job_id_out=batch_sort_jobid --cmd="$batch_sort_cmd"

#     fastq_regions_cmd=$(cat <<-EOF
#         GrassSV.py filter_reads -f1 ${filtered_reads1_file} -f2 ${filtered_reads2_file} -s ${sorted_alignments_file} -ss ${sorted_alignments_file} -roi ${roi} > ${work_dir}/filter_reads_${read_num}.txt
# EOF
#     )

#     submit_job --job-name="fastq_regions_${read_num}" --dependency="afterok:$batch_sort_jobid" --cmd="$fastq_regions_cmd" --job_id_out=fastq_regions_jobid
#     fastq_regions_jobids+=($fastq_regions_jobid)
# done

# merge_filtered_reads_cmd=$(cat <<-EOF
#     cat ${work_dir}/filtered_reads1_*.fastq > ${filtered_reads1}
#     cat ${work_dir}/filtered_reads2_*.fastq > ${filtered_reads2}
# EOF
# )

# #--dependency="afterok:${fastq_regions_jobids[*]}"
# submit_job --job-name="merge_filtered_reads" --cmd="$merge_filtered_reads_cmd" --job_id_out=merge_filtered_reads_jobid

# alga_cmd="$scriptDir/run_alga.sh > $work_dir/run_alga.txt"
# submit_job --job-name="alga" --dependency="afterok:$merge_filtered_reads_jobid" --cmd="$alga_cmd" --job_id_out=alga_jobid

#--dependency="afterok:$alga_jobid"
quast_cmd="$scriptDir/run_quast.sh > $work_dir/run_quast.txt"
submit_job --job-name="quast" --cmd="$quast_cmd" --job_id_out=quast_jobid

find_sv_cmd="GrassSV.py find_sv $quast_alignments -o $results > $work_dir/find_sv.txt"
submit_job --job-name="find_sv" --dependency="afterok:$quast_jobid" --cmd="$find_sv_cmd" --job_id_out=find_sv_jobid

find_hdr_cmd="GrassSV.py find_hdr $coverage_file $results/duplications.bed > $work_dir/find_hdr.txt"
submit_job --job-name="find_hdr" --cmd="$find_hdr_cmd" --job_id_out=find_hdr_jobid

Add SLURM job IDs to an array for reference or further processing
job_ids=("$merge_filtered_reads_jobid" "$alga_jobid" "$quast_jobid" "$find_sv_jobid" "$find_hdr_jobid")

# Print the job IDs
for job_id in "${job_ids[@]}"; do
    echo "Scheduled job with ID: $job_id"
done