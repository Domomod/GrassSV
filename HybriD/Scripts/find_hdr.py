import numpy as np

from HybriD.Region.DepthRegion import DepthRegion

WINDOW = 70  # TODO: wszystkie parametry jako opcjonalne do ustawienia
THRESHOLD = 40
MIN_CONSECUTIVE_REGION = 1000   # Min length of SV


def find_hdr():  # TODO: dopisz sprawdzanie czy plik istnieje, jeżeli tak to go usuń
    singleChromosome = []
    chromosomes = []
    start_of_file = "/home/krzysztof/illumina_dane/duplikacje/10"
    with open(f"{start_of_file}/depth.coverage") as file:  # TODO: porozdzielaj na funkcje
        s = [i.split() for i in file.readlines()]
        if s.count([]) > 0:
            s.remove([])
        th = np.median(np.array(s)[:, 2].astype(int))
        for line in s:
            if len(singleChromosome) != 0 and line[0] != singleChromosome[0][0]:
                chromosomes.append(singleChromosome)
                singleChromosome = []
            singleChromosome.append(line)
        chromosomes.append(singleChromosome)
    THRESHOLD = th + 10
    for chromosome in chromosomes:
        chromosome_depth = [int(i[2]) for i in chromosome]
        arr = np.array(
            [np.array(chromosome_depth[i - WINDOW:i]).mean() for i in range(WINDOW, len(chromosome_depth), WINDOW)])
        last = arr[0]
        consecutive = 0
        regions_to_serialize: [DepthRegion] = []
        curr_start = 0
        for x, i in enumerate(arr):
            if i > THRESHOLD and consecutive == 0:
                curr_start = (x - 1) * WINDOW
                curr_start = 0 if curr_start < 0 else curr_start
            if THRESHOLD < i:
                consecutive += 1
            else:
                consecutive = 0
            if last > THRESHOLD and consecutive == 0:
                if (x + 1) * WINDOW - curr_start > MIN_CONSECUTIVE_REGION:
                    regions_to_serialize.append(DepthRegion(chromosome[0][0], curr_start, (x + 1) * WINDOW))
            last = i
        serialize(regions_to_serialize, f"{start_of_file}/duplications.bed")


def serialize(depthRegions: [DepthRegion], fileName: str):
    with open(fileName, 'a+') as file:
        for depthRegion in depthRegions:
            file.write(str(depthRegion))


if __name__ == "__main__":
    find_hdr()
