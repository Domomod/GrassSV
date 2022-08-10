#!/usr/bin/python3
import sys
import os

def split_bed_per_type(mutations, out_dir="generated_mutations"):
    os.makedirs(out_dir, exist_ok =True)
    with open(out_dir+"/deletions.bed", "w") as deletions, \
         open(out_dir+"/duplications.bed", "w") as duplications, \
         open(out_dir+"/insertions.bed", "w") as insertions, \
         open(out_dir+"/inversions.bed", "w") as inversions, \
         open(out_dir+"/translocations.bed", "w") as translocations, \
         open(mutations, "r") as file:
        for line_str in file:
            line = line_str.split()

            chromosome=line[0],
            start=int(line[1]),
            end=int(line[2])
            type=line[3]           
            if   type.startswith("DEL"):
                deletions.write(line_str)
            elif type.startswith("DUP"):
                duplications.write(line_str)
            elif type.startswith("INS"):
                insertions.write(line_str)
            elif type.startswith("INV"):
                inversions.write(line_str)
            elif type.startswith("TRA"):
                translocations.write(line_str)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        split_bed_per_type(sys.argv[1],sys.argv[2])
    elif len(sys.argv) == 2:
        split_bed_per_type(sys.argv[1])
    else:
        print("Not enough arguments")