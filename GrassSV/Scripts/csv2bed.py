#!/usr/bin/python3

import os

def export_to_bed(input_path, output_path):
    print("\033[0;36m" #Light Cyan
          f"[+]Exporting vcf file: \"{input_path}\" to \"{output_path} bed format file."
          "\033[0m")

    from GrassSV.Alignment import load_vcf, alignments
    sv = load_vcf.load_vcf(input_path)
    alignments.export_records(sv, output_path = output_path)
    
    print("\033[1;32m" #Bold green
          f"[+]File exporting of \"{input_path}\" to \"{output_path} succesfull"
          "\033[0m")