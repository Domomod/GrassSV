
def find_roi(inputPath, outputPath, maxCoverage, marginSize=150, minSize=1):
    chromosomes = []
    singleChromosome = []
    inputFile = open(inputPath, "r")
    for line in inputFile:
        words = line.split()
        if (len(singleChromosome) != 0 and words[0] != singleChromosome[0][0]):  # new chromosome
            chromosomes.append(singleChromosome)
            singleChromosome = []
        singleChromosome.append(words)
    chromosomes.append(singleChromosome)
    inputFile.close()
    endings = []
    for chromosome in chromosomes:
        inLowCoverageRegion = False
        LowCoverageBegining = 0
        LowCoverageSize = 0
        for number in range(len(chromosome)):
            if (int(chromosome[number][2]) <= maxCoverage):
                if (inLowCoverageRegion == False):
                    LowCoverageBegining = number
                    inLowCoverageRegion = True
                LowCoverageSize += 1
                if (number == len(chromosome) - 1):  # end of region can appear on the last element
                    if (LowCoverageSize >= minSize):
                        begining = chromosome[max(LowCoverageBegining-marginSize, 0)]
                        begining.append("B")  # begining of region
                        ending = chromosome[number] #it's the end
                        ending.append("E")  # end of region
                        inLowCoverageRegion = False
                        LowCoverageSize = 0
                        endings.append(begining)
                        endings.append(ending)
            else:
                if (inLowCoverageRegion):
                    if (LowCoverageSize >= minSize):
                        begining = chromosome[max(LowCoverageBegining-marginSize,0)]
                        begining.append("B")  # begining of region
                        ending = chromosome[min(number - 1+marginSize,len(chromosome)-1)]
                        ending.append("E")  # end of region
                        endings.append(begining)
                        endings.append(ending)
                    inLowCoverageRegion = False
                    LowCoverageSize = 0
    del chromosome
    del chromosomes
    lastIteration=len(endings)
    for i in range(len(endings)):
        for number in range(len(endings)):
            if ( number< len(endings)-3 and endings[number][3]=="E" and endings[number][0]==endings[number+1][0]): #ending checks if next one is on the same chromosome
                if (int(endings[number][1])>=int(endings[number+1][1]) or int(endings[number][1])+1==int(endings[number+1][1])): #if last region ending point is higher than begining of the next one or one starts when the second one ends- merge them in one
                    del endings[number]
                    del endings[number]
        if (len(endings)==lastIteration):
            break
        lastIteration=len(endings)
    outputFile = open(outputPath, "w")
    for line in endings:
        outputFile.write(line[0]+"\t"+line[1]+"\t"+line[2]+"\n")
    outputFile.close()


def run(input_file, output_file, limit_coverage, margin_size, minimum_size):
    find_roi(input_file, output_file, limit_coverage,margin_size, minimum_size)