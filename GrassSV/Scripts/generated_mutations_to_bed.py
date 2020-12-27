import os
import pandas
def correct_ref_name(ref):
    ref = list(ref)
    ref[3] = '|'
    ref[-1] = '|'
    ref = ''.join(ref)
    return ref

def write_regular_mutations(data, file, file_name):
    for idx, row in data.iterrows():
        chromosome = row['Chr'].split(' ', 1)[0]
        chromosome = correct_ref_name(chromosome)
        start = row['Start']
        end = row['End']
        region_name = row['Name']

        file.write(" ".join([
            chromosome, str(start), str(end), file_name
        ])+ "\n")

def write_translocations(data, file, file_name):
    for idx, row in data.iterrows():
        chromosome = row['ChrA'].split(' ', 1)[0]
        chromosome = correct_ref_name(chromosome)
        start = row['StartA']
        end = row['EndA']

        file.write(" ".join([
            chromosome, str(start), str(end), file_name
        ]) + "\n")

        chromosome = row['ChrB'].split(' ', 1)[0]
        chromosome = correct_ref_name(chromosome)
        start = row['StartB']
        end = row['EndB']

        file.write(" ".join([
            chromosome, str(start), str(end), file_name
        ]) + "\n")

def run(csv_paths, bed_path):
    with open(bed_path, 'w') as file:
        for csv_path in csv_paths:
            basename= os.path.basename(csv_path)
            basename = os.path.splitext(basename)[0]

            data = pandas.read_csv(csv_path, sep='\t')
            if 'Chr' in data.columns: #quast format for deletion, inversions, insertions
                write_regular_mutations(data, file, basename)
            elif 'ChrA' in data.columns: #quast format for translocations
                write_translocations(data, file, basename)
