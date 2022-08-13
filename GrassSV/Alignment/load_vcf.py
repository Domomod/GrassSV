from GrassSV.Alignment.alignments import TranslocationPattern, Pattern
import re

def load_vcf(path):
    patterns = []
    with open(path, "r") as file:
        for line in file:
            if line.startswith('#'):
                continue
            line = line.split()


            chromosome=line[0]

            pos=int(line[1]) - 1 #Convert from 1 based to 0 based system 

            info=line[7]
            m = re.match(r'END=([0-9]*);', info, re.M|re.I)
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