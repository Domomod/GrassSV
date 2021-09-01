#!/bin/bash

if [[ ! -d $GRASSUTILS || -z $GRASSUTILS ]]
then
	echo "To use this tool, please specify GRASSUTILS variable to point to this file location. GRASSUTILS: $GRASSUTILS"
	exit 
fi



MUTATION_FOLDER=${2:=../mutations/fastadna_deletions}
SV_TYPE=${1:=2}
GENOME=ref.fsa

mkdir -p ${MUTATION_FOLDER}
mkdir -p ${MUTATION_FOLDER}/log
cp ${GENOME} ${MUTATION_FOLDER}/genome.fsa
jid1=$(${GRASSUTILS}/smart_sbatch -J gen_mutation -e ${MUTATION_FOLDER}/log/gen_mutation.err -o ${MUTATION_FOLDER}/log/gen_mutation.out ${GRASSUTILS}/multiple.sh ${SV_TYPE} ${MUTATION_FOLDER}/genome.fsa temp_${SV_TYPE} ${MUTATION_FOLDER}/out.bed)
echo "Submitted gen_mutations step | jid $jid1"
:
jid2=$(${GRASSUTILS}/smart_sbatch --dependency=afterany:${jid1} -J run_art -e ${MUTATION_FOLDER}/log/run_art.err -o ${MUTATION_FOLDER}/log/run_art.out ${GRASSUTILS}/run_art.sh ${MUTATION_FOLDER})
echo "Submitted run_art step | jid $jid2"

jid3=$(${GRASSUTILS}/smart_sbatch --dependency=afterany:${jid2} -J calculate_depth.sh -e ${MUTATION_FOLDER}/log/calculate_depth.err -o ${MUTATION_FOLDER}/log/calculate_depth.out ${GRASSUTILS}/calculate_depth.sh ${MUTATION_FOLDER})
echo "Submitted calculate_depth step | jid $jid3"

jid4=$(${GRASSUTILS}/smart_sbatch --dependency=afterany:${jid3} -J extract_reads -e ${MUTATION_FOLDER}/log/extract_reads.err -o ${MUTATION_FOLDER}/log/extract_reads.out ${GRASSUTILS}/whole_pipeline.sh ${MUTATION_FOLDER})
echo "Submitted extract_reads step | jid $jid4"

jid5=$(${GRASSUTILS}/smart_sbatch --dependency=afterany:${jid4} -J run_grasshopper -e ${MUTATION_FOLDER}/log/run_grasshopper.err -o ${MUTATION_FOLDER}/log/run_grasshopper.out ${GRASSUTILS}/whole_pipeline2.sh ${MUTATION_FOLDER})
echo "Submitted run_grasshopper step | jid $jid5"

jid6=$(${GRASSUTILS}/smart_sbatch --dependency=afterany:${jid5} -J run_quast -e ${MUTATION_FOLDER}/log/run_quast.err -o ${MUTATION_FOLDER}/log/run_quast.out ${GRASSUTILS}/whole_pipeline3.sh ${MUTATION_FOLDER})
echo "Submitted run_quast step |jid $jid6"

jid5_2=$(${GRASSUTILS}/smart_sbatch --dependency=afterany:${jid4} -J run_alga -e ${MUTATION_FOLDER}/log/run_alga.err -o ${MUTATION_FOLDER}/log/run_alga.out ${GRASSUTILS}/whole_pipeline2_alga.sh ${MUTATION_FOLDER})
echo "Submitted run_alga step | jid $jid5_2"

jid6_2=$(${GRASSUTILS}/smart_sbatch --dependency=afterany:${jid5_2} -J run_quast_alga -e ${MUTATION_FOLDER}/log/run_quast_alga.err -o ${MUTATION_FOLDER}/log/run_quast_alga.out ${GRASSUTILS}/whole_pipeline3.sh ${MUTATION_FOLDER} alga contigs.fasta_contigs.fasta)
echo "Submitted run_quast (alga) step |jid $jid6_2"
