#!/usr/bin/python3

import sys

size = 0
increment_size = 500

increment_every_count = 100 # 50 for one cv type only, 100 for translocations only, 60 for all cv types  

if __name__ == "__main__":
    increment_id = 0
    with open(sys.argv[2], "w") as out_file, \
         open(sys.argv[1], "r") as file:
        for line in file:
            line = line.split()

            size += increment_size if increment_id % increment_every_count == 0 else 0
            increment_id +=1
            
            chromosome=line[0]
            start=int(line[1])
            end=int(start)+size
            cv_type=(line[3])
            if "TRANS:TO" in cv_type or "INS" in cv_type:
                end = start + 1

            out_file.write(f"{chromosome} {start} {end} {cv_type}\n")

                    