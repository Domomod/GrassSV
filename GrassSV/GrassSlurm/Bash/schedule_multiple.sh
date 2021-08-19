#!/bin/bash

FILENAME=${1:-ref.fsa}
FOLDERPREFIX=${2:-Fastadna}
if [ ! -f $FILENAME ]
then
	echo "Genome file path wrong"
	exit
fi

if [[ ! -d $GRASSUTILS || -z $GRASSUTILS ]]
then
	echo "To use this tool, please specify GRASSUTILS variable to point to this file location. GRASSUTILS: $GRASSUTILS"
	exit 
fi

#mkdir -p ${FOLDERPREFIX}_all
mkdir -p ${FOLDERPREFIX}_translocations
mkdir -p ${FOLDERPREFIX}_insertions
mkdir -p ${FOLDERPREFIX}_deletions
mkdir -p ${FOLDERPREFIX}_inversions
mkdir -p ${FOLDERPREFIX}_duplications

#cp $FILENAME ${FOLDERPREFIX}_all/$FILENAME
cp $FILENAME ${FOLDERPREFIX}_translocations/$FILENAME
cp $FILENAME ${FOLDERPREFIX}_insertions/$FILENAME
cp $FILENAME ${FOLDERPREFIX}_deletions/$FILENAME
cp $FILENAME ${FOLDERPREFIX}_inversions/$FILENAME
cp $FILENAME ${FOLDERPREFIX}_duplications/$FILENAME

#sbatch -J gen_all $GRASSUTILS/multiple.sh -1 ${FOLDERPREFIX}_all/$FILENAME temp_-1.fsa ${FOLDERPREFIX}_all/out.bed
sbatch -J gen_tra $GRASSUTILS/multiple.sh 0 ${FOLDERPREFIX}_translocations/$FILENAME temp_0.fsa ${FOLDERPREFIX}_translocations/out.bed
sbatch -J gen_ins $GRASSUTILS/multiple.sh 1 ${FOLDERPREFIX}_insertions/$FILENAME temp_1.fsa ${FOLDERPREFIX}_insertions/out.bed
sbatch -J gen_del $GRASSUTILS/multiple.sh 2 ${FOLDERPREFIX}_deletions/$FILENAME temp_2.fsa ${FOLDERPREFIX}_deletions/out.bed
sbatch -J gen_inv $GRASSUTILS/multiple.sh 3 ${FOLDERPREFIX}_inversions/$FILENAME temp_3.fsa ${FOLDERPREFIX}_inversions/out.bed
sbatch -J gen_dup $GRASSUTILS/multiple.sh 4 ${FOLDERPREFIX}_duplications/$FILENAME temp_4.fsa ${FOLDERPREFIX}_duplications/out.bed
