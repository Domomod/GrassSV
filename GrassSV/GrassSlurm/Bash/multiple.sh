#!/bin/bash

if [[ ! -d $GRASSUTILS || -z $GRASSUTILS ]]
then
        echo "To use this tool, please specify GRASSUTILS variable to point to this file location"
        exit
fi

module load python/3.8.8
echo "Job started"
python3 $GRASSUTILS/multiple.py $1 $2 $3 $4
echo "Job ended with code {$?}"
