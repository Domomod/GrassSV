from GrassSV.Alignment.alignments import Pattern


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