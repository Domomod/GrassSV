from HybriD.Alignment.pattern import Pattern

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
    realStartOfCurrentChromosome=0
    realCurrent=0
    simStartOfCurrentChromosome=0
    simCurrent=0
    found=0
    while (realCurrent<len(realtab)):
        if realtab[realStartOfCurrentChromosome].chromosome!=realtab[realCurrent].chromosome:
            realStartOfCurrentChromosome=realCurrent #starting a new chromosome in both tabs
            simStartOfCurrentChromosome=simCurrent
            while (simStartOfCurrentChromosome< len(simtab) and simtab[simStartOfCurrentChromosome].chromosome<realtab[realStartOfCurrentChromosome].chromosome):
                simStartOfCurrentChromosome+=1
                simCurrent=simStartOfCurrentChromosome
        while (simCurrent<len(simtab) and simtab[simCurrent].chromosome==realtab[realCurrent].chromosome):
            if calculate_single_pair(realtab[realCurrent],simtab[simCurrent]) >= percentage:
                found +=1
            simCurrent+=1
        simCurrent=simStartOfCurrentChromosome #setting to begining of this chromosome
        realCurrent+=1
    return found/len(realtab)*100


if __name__=="__main__":
    tab1=[
        Pattern("chr1", 1,200), #not intersecting, second inversed N
        Pattern("chr2", 1,200), #intersecting, second inversed Y
        Pattern("chr3",50,150), #50% N
        Pattern("chr4",200,400), #>90% Y
    ]
    tab2=[
        Pattern("chr1",300,200),
        Pattern("chr2", 200,1),
        Pattern("chr3", 100,150),
        Pattern("chr4", 210,400)
    ]
    print(calculate_type(tab1,tab2,90))