from HybriD.Alignment.pattern import Pattern
from HybriD.Alignment.load_bed import  load_pattern_bed
from HybriD.Alignment.load_csv import load_regular, load_translocation_as_separate_patterns
def calculate_single_pair(first, second):
    if first.chromosome!=second.chromosome:
        return 0
    first_start=min(first.start, first.end)
    first_end=max(first.end, first.start)
    second_start=min(second.start, second.end)
    second_end=max(second.end, second.start)
    if first_start>second_end or second_start>first_end:
        return 0 #not intersecting
    sizeOfAll=max(first_end,second_end)-min(first_start,second_start)
    sizeOfIntersection=min(first_end,second_end)-max(first_start,second_start)
    return sizeOfIntersection/sizeOfAll*100

def calculate_type(realtab, simtab, percentage):
    found=0

    for real in realtab:
        for simulated in simtab:
            if calculate_single_pair(real, simulated) >= percentage:
                found +=1
    return str(found)+"/"+str(len(realtab))



if __name__=="__main__":
    pierwsze=load_translocation_as_separate_patterns("translocations.csv")
    drugie=load_pattern_bed("deletions_contig_patterns.bed")

    print(calculate_type(pierwsze,drugie,90))
    print(calculate_type(pierwsze,drugie,70))
    print(calculate_type(pierwsze,drugie,50))
    print(calculate_type(pierwsze,drugie,10))