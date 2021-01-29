from GrassSV.Alignment.alignments import Pattern, do_they_intersect, sort_coords
from GrassSV.Scripts.load_files import load_prawdziwe, load_grassv_translocation, load_manta, load_grassv, \
    load_sniffless, load_cnvnator, load_rsvsim_trans, load_rsvsim
from GrassSV.Alignment.load_csv import load_regular, load_translocation_as_separate_patterns, load_translocation


def calculate_single_pair(first, second):
    if first.chromosome != second.chromosome:
        return 0
    if not do_they_intersect(first, second):
        return 0  # not intersecting
    outerleft, innerleft, innerright, outerright = sort_coords(first, second)
    sizeOfIntersection = innerright - innerleft
    sizeOfAll=outerright-outerleft
    return sizeOfIntersection / sizeOfAll * 100 if sizeOfAll!=0 else 0


def calculate_type(realtab, simtab, percentage):
    found = 0
    for real in realtab:
        for simulated in simtab:
            if calculate_single_pair(real, simulated) >= percentage:
                found += 1
    return str(found) + "/" + str(len(realtab))


def calculate_pair_of_translocations(first, second, margin):
    destination = calculate_insertions(first.destination, second.destination, margin)
    source = calculate_single_pair(first.source, second.source)
    if destination == True:
        return source
    return 0


def calculate_all_translocations(realtab, simtab, percentage):
    found = 0
    margin = 0
    if percentage == 95:
        margin = 5
    if percentage == 90:
        margin = 5
    if percentage == 80:
        margin = 10
    for real in realtab:
        for simulated in simtab:
            if calculate_pair_of_translocations(real, simulated, margin) >= percentage:
                found += 1
    return str(found) + "/" + str(len(realtab))


def calculate_insertions(first, second, margin):
    if not first.start <= second.start:
        first, second = second, first
    same_chromosome = first.chromosome == second.chromosome
    start_coordinates = abs(first.start - second.start) < margin
    end_coordinates = abs(first.end - second.end) < margin
    return same_chromosome and start_coordinates and end_coordinates


def calculate_all_insertions(realtab, simtab, margin):
    found = 0
    for real in realtab:
        for simulated in simtab:
            if calculate_insertions(real, simulated, margin):
                found += 1
    return str(found) + "/" + str(len(realtab))


if __name__ == "__main__":
    folders = ["dane/ostateczne/", "dane/rsvsim/"]
    rsvsim = ["deletions.csv", "insertions.csv", "inversions.csv", "tandemDuplications.csv"]
    ostateczne = ["delicje.bed", "duplikacje.bed", "insertion.bed", "inwersje.bed", "translokacje.bed"]
    rsvsimtest = ["deletions.bed", "translocations.bed", "filter_inversions.bed", "duplications.bed"]
    ostatecznetest = ["deletions.bed", "duplications.bed", "insertion.bed", "filter_inversions.bed",
                      "translocations.bed"]
    sniff = load_grassv_translocation("dane/rsvsim/translocations.bed")
    grasss= load_translocation("dane/rsvsim/prawdziwe/insertions.csv")

    print(calculate_all_translocations(grasss, sniff, 90))
    # for percentage in [95,90,80]:
    #    for i in range(len(rsvsim)):
    #        print(rsvsimtest[i])
    #        dane_path=folders[1]+"prawdziwe/"+rsvsim[i]
    #        grass_path=folders[1]+"detectedSVs/"+rsvsimtest[i]
    #        if (rsvsim[i]=="insertions.csv"):
    #            dane=load_translocation(dane_path)
    #            grass=load_grassv_translocation(grass_path)
    #            print(calculate_all_translocations(dane,grass,percentage))
    #            print(calculate_all_translocations(grass, grass, percentage))
    #        else:
    #            dane=load_regular(dane_path)
    #            grass=load_grassv(grass_path)
    #            print(calculate_type(dane,grass,percentage))
