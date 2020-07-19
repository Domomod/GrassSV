import sys
import pandas
def correct_ref_name(ref):
    ref = list(ref)
    ref[3] = '|'
    ref[-1] = '|'
    ref = ''.join(ref)
    return ref
with open(sys.argv[2], 'w') as file:
    data = pandas.read_csv(sys.argv[1], sep='\t')
    for idx, row in data.iterrows():
        chromosome = row['Chr'].split(' ', 1)[0]
        chromosome = correct_ref_name(chromosome)
        start=row['Start']
        end=row['End']
        region_name=row['Name']

        file.write(" ".join([
            chromosome, str(start), str(end)
        ]))