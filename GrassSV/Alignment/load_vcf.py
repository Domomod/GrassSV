from GrassSV.Alignment.alignments import TranslocationPattern, Pattern
import re

CHROM_ID = None
POS_ID   = None
INFO_ID  = None
prev_line = None
def load_vcf(path):
    patterns = []
    with open(path, "r") as file:
        for line in file:
            if line.startswith('##'):
                continue

            if len(line.strip()) == 0 :
                continue

            if line.startswith('#'):
                COLUMNS = line.split()

                global CHROM_ID
                global POS_ID
                global INFO_ID

                CHROM_ID = [idx for idx, s in enumerate(COLUMNS) if "CHROM" in s][0]
                POS_ID = [idx for idx, s in enumerate(COLUMNS) if "POS" in s][0]
                INFO_ID = [idx for idx, s in enumerate(COLUMNS) if "INFO" in s][0]

                print(f"VCF format is \"{COLUMNS}\"")
                print(f"Choromosome column: {CHROM_ID}")
                print(f"Position column: {POS_ID}")
                print(f"Info column: {INFO_ID}")

                continue

            line = line.split()

            chromosome=line[CHROM_ID]

            info=line[INFO_ID]

            global prev_line
            if None != re.match(r'^(.*;)?SVTYPE=BND;', info, re.M|re.I):
                m = re.match(r'.*EVENT=(.*);', info, re.M|re.I)

                if None == prev_line:
                    prev_line = line
                    continue
                else:
                    chromosome = line[CHROM_ID]
                    pos=int(prev_line[POS_ID]) - 1 #Convert from 1 [pos, end] based to 0 based system [pos, end)
                    end=int(line[POS_ID])

                    prev_line = None
            else:
                m = re.match(r'.*END=([0-9]*);', info, re.M|re.I)
                pos=int(line[POS_ID]) #Convert from 1 [pos, end] based to 0 based system [pos, end)
                end=int(m.group(1))

            patterns.append(Pattern(
                chromosome=chromosome,
                start=pos,
                end=end
            ))
    return patterns

#def load_translocations_bed(path):
#    patterns = []
#    with open(path, "r") as file:
#        while True:
#            line1 = file.readline().split()
#            line2 = file.readline().split()
#            if not line2: break
#
#            patterns.append(
#                TranslocationPattern(
#                    source = Pattern(
#                        chromosome=line1[0],
#                        start=int(line1[1]),
#                        end=int(line1[2])
#                    ),
#                    destination= Pattern(
#                        chromosome=line2[0],
#                        start=int(line2[1]),
#                        end=int(line2[2])
#                    )
#                )
#            )
#    return patterns