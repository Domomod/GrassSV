import numpy as np

from GrassSV.Region.DepthRegion import DepthRegion

TEXT = 'find_hdr'


def find_hdr(input_file, output_file, window=70, threshold=None, min_consecutive_region=1000):
    chromosomes, threshold = read_input_file(input_file, threshold)
    possible_regions = find_possible_regions(chromosomes, min_consecutive_region, threshold, window)
    possible_regions = connect_consecutive_regions(possible_regions, min_consecutive_region)
    serialize(possible_regions, output_file)


def read_input_file(input_file, threshold):
    singleChromosome = []
    chromosomes = []
    with open(input_file) as file:
        s = [i.split() for i in file.readlines()]
        if s.count([]) > 0:
            s.remove([])
        if not threshold:
            th = np.median(np.array(s)[:, 2].astype(int))
            std = np.std(np.array(s)[:, 2].astype(int))
        for line in s:
            if len(singleChromosome) != 0 and line[0] != singleChromosome[0][0]:
                chromosomes.append(singleChromosome)
                singleChromosome = []
            singleChromosome.append(line)
        chromosomes.append(singleChromosome)
    if not threshold:
        threshold = th + std
    return chromosomes, threshold


def find_possible_regions(chromosomes, min_consecutive_region, threshold, window):
    regions_to_serialize: [DepthRegion] = []
    for chromosome in chromosomes:
        chromosome_depth = [int(i[2]) for i in chromosome]
        arr = np.array(
            [np.array(chromosome_depth[i - window:i]).mean() for i in range(window, len(chromosome_depth), window)])
        last = arr[0]
        consecutive = 0
        curr_start = 0
        for x, i in enumerate(arr):
            if i > threshold and consecutive == 0:
                curr_start = (x - 1) * window
                curr_start = 0 if curr_start < 0 else curr_start
            if threshold < i:
                consecutive += 1
            else:
                consecutive = 0
            if last > threshold and consecutive == 0:
                if (x + 1) * window - curr_start > min_consecutive_region:
                    regions_to_serialize.append(DepthRegion(chromosome[0][0], curr_start, (x + 1) * window))
            last = i
    return regions_to_serialize


def connect_consecutive_regions(regions: [DepthRegion], min_consecutive_region):
    regions = sorted(regions, key=lambda x: (x.chromosome, x.start, x.end))
    index = 0
    while index < len(regions) - 1:
        first = regions[index]
        second = regions[index + 1]
        sub = second - first
        if first.chromosome == second.chromosome and abs(sub) <= min_consecutive_region:
            if sub < 0:
                regions[index] = DepthRegion(first.chromosome, second.start, first.end)
            elif sub > 0:
                regions[index] = DepthRegion(first.chromosome, first.start, second.end)
            else:
                regions[index] = DepthRegion(first.chromosome, min(first.start, second.start),
                                             max(first.end, second.end))
            del regions[index + 1]
        else:
            index += 1
    return regions


def serialize(depthRegions: [DepthRegion], fileName: str):
    with open(fileName, 'w') as file:
        for depthRegion in depthRegions:
            file.write(str(depthRegion))
