import pandas as pd
from HybriD.Region.BioRegion import Region
from HybriD.Region.BioRegion import RegionComposite

def load_our_finder(filename):
    data = pd.read_csv(filename)
    record_set = []
    for idx, row in data.iterrows():
        ref = row['Reference']
        ref = correct_ref_name(ref)
        region = Region(start=row['Start'],
                        end=row['End'],
                        ref=ref,
                        region_name=row["Name"],
                        region_type=''.join([str.lower(i) for i in row["Name"] if not i.isdigit()]),
                        qualifiers={'length': int(row["Length"])}
                        )

        record_set.append(region)

        if __name__ == "__main__" and idx < 2:
            print(region, end='\n')

    return record_set


def load_deletions(filename, type='deletion'):
    # RSVsim collumn names for deletions:
    # Name, Chr, Start, End, Size, BpSeqx
    data = pd.read_csv(filename, sep='\t')
    record_set = []
    for idx, row in data.iterrows():
        ref = row['Chr'].split(' ', 1)[0]
        ref = correct_ref_name(ref)
        region = Region(start=row['Start'],
                        end=row['End'],
                        ref=ref,
                        region_name=row['Name'],
                        region_type=type,
                        qualifiers={'length': int(row["Size"])}
                        )

        record_set.append(region)

        if __name__ == "__main__" and idx < 2:
            print(region, end='\n')

    return record_set


def load_inversions(filename):
    # Files generated for inversions and deletions are identical
    return load_deletions(filename, type="inversion")


def load_translocations(filename):
    # RSVsim collumn names for translocations:
    # Name	ChrA	StartA	EndA	ChrB	StartB	EndB
    # Size	Copied	BpSeqA	BpSeqB_5prime	BpSeqB_3prime

    data = pd.read_csv(filename, sep='\t')
    record_set = []
    for idx, row in data.iterrows():
        ref_a = row['ChrA'].split(' ', 1)[0]
        ref_a = correct_ref_name(ref_a)
        ref_b = row['ChrB'].split(' ', 1)[0]
        ref_b = correct_ref_name(ref_b)
        region1 = Region(start=row['StartA'],
                         end=row['EndA'],
                         ref=ref_a,
                         region_type='translocation_part',
                         qualifiers={'origin': "from"}
                         )

        region2 = Region(start=row['StartB'],
                         end=row['EndB'],
                         ref=ref_b,
                         region_type='translocation_part',
                         qualifiers={'origin': "to"}
                         )

        region_composite = RegionComposite(regions=[region1, region2],
                                           region_name=row['Name'],
                                           region_type='translocation',
                                           qualifiers={'length': int(row["Size"])}
                                           )

        record_set.append(region_composite)

        if __name__ == "__main__" and idx < 2:
            print(region_composite, end='\n')

    return record_set


def load_tandem_duplications(filename):
    # RSVsim collumn names for tandem dups:
    # Name, Chr, Start, End, Size, Duplications, BpSeqx

    data = pd.read_csv(filename, sep='\t')
    record_set = []

    for idx, row in data.iterrows():
        ref = row['Chr'].split(' ', 1)[0]
        ref = correct_ref_name(ref)
        region = Region(start=row['Start'],
                        end=row['End'],
                        ref=ref,
                        region_name=row['Name'],
                        region_type='tandem-duplcation',
                        qualifiers={'length': int(row["Size"]),
                                    'duplications': int(row["Duplications"])}
                        )

        record_set.append(region)

        if __name__ == "__main__" and idx < 2:
            print(region, end='\n')

    return record_set


#
def correct_ref_name(ref):
    ref = list(ref)
    ref[3] = '|'
    ref[-1] = '|'
    ref = ''.join(ref)
    return ref


# Preview of functions declared inside this file

if __name__ == "__main__":
    load_deletions("data/generated-mutations/deletions.csv")
    load_translocations("data/generated-mutations/insertions.csv")
    load_inversions("data/generated-mutations/inversions.csv")
    load_tandem_duplications("data/generated-mutations/tandemDuplications.csv")
