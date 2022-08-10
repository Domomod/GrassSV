from GrassSV.Alignment.alignments import TranslocationPattern, Pattern


def load_pattern_bed(path):
    patterns = []
    with open(path, "r") as file:
        for line in file:
            line = line.split()

            patterns.append(Pattern(
                chromosome=line[0],
                start=int(line[1]),
                end=int(line[2])
            ))
    return patterns

def load_translocations_bed(path):
    patterns = []
    with open(path, "r") as file:
        while True:
            line1 = file.readline().split()
            line2 = file.readline().split()
            if not line2: break

            patterns.append(
                TranslocationPattern(
                    source = Pattern(
                        chromosome=line1[0],
                        start=int(line1[1]),
                        end=int(line1[2])
                    ),
                    destination= Pattern(
                        chromosome=line2[0],
                        start=int(line2[1]),
                        end=int(line2[2])
                    )
                )
            )
    return patterns