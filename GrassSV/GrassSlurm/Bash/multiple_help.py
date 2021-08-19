#!/usr/bin/python3
import sys

if __name__ == '__main__':
        print("""python3 multiples.py sv_type FILE TEMP_FILE
========================USAGE========================
    -sv_type int         1:all 0:translocations 1:insert 2:delete 3:invert 4:duplications
    -FILE string         genome file (this is both your initial input, and your designated output)
    -TEMP_FILE string    temporary genom file name (use diffrent names for concurrent use)
""")
