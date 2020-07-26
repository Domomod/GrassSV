
#This function takes sizes of chromosomes from input_path
#and saves it in output_path
def chromosomesSizes(input_path, output_path):
    input_file=open(input_path,"r")
    output_file = open(output_path, "w")
    for line in input_file:
        words=line.split()
        if (words[0]=="@SQ"):
            lenght = words[2].split(':')[1]
            chromosome_name = words[1].split(':')[1]
            output_file.write(chromosome_name+' '+lenght+'\n')
    input_file.close()
    output_file.close(1219438)


#This function marks (set 4th paramether of every line to true) reads
#which are nearby low coverage region
def markLowCoverageRegion(chromosome, firstInLowCoverage, lastInLowCoverage):
    startWriting=max(0,firstInLowCoverage-150)
    stopWriting=min(len(chromosome)-1,lastInLowCoverage+150) #last possible
    for iterator in range(startWriting,stopWriting):
        chromosome[iterator][3]=True
    return chromosome

#This function writes marked lines from chromosome to an output file
def printChromosome(chromosome,output_file):
    output=open(output_file,"a")
    for i in range(len(chromosome)):
        if (chromosome[i][3]==True and (i==0 or chromosome[i-1][3]==False)):
            output.write(chromosome[i][0]+"\t"+chromosome[i][1]+"\t")
        if (chromosome[i][3]==True and (i+1==len(chromosome) or chromosome[i+1][3]==False)):
            output.write((chromosome[i][1])+"\n")

#This function search for low coverage regions on a single chromosome
def checkSingleChromosome(chromosome,limit,output_file):
    startOfLowCoverageFound = False
    for number in range(len(chromosome)):
        if (int(chromosome[number][2])<=limit):
            if (startOfLowCoverageFound==False):
                startOfLowCoverageFound=True
                firstInLowCoverage=number
        else:
            if (startOfLowCoverageFound==True):
                startOfLowCoverageFound=False
                lastInLowCoverage=number-1
                chromosome=markLowCoverageRegion(chromosome, firstInLowCoverage, lastInLowCoverage)
    printChromosome(chromosome,output_file)


#This function cuts genome into single chromosomes and then checks
#low coverage region in chromosomes one by one
def cutIntoSingleChromosome(input_path,limit,output_file):
    input_file=open(input_path,"r")
    chromosome=[]
    for line in input_file:  #File format: chromosome name  number of nucleotydes   coverage
        words=line.split()
        words.append(False)  #is nearby 0 coverage region; defalult false
        if (len(chromosome)==0): #the function just started no word was yet added
            chromosome.append(words)
            continue
        if (chromosome[0][0]==words[0]): #it's next nucleotide on the same chromosome
            chromosome.append(words)
            continue
        if (chromosome[0][0]!=words[0]):
            checkSingleChromosome(chromosome,limit,output_file)
            chromosome=[]
            chromosome.append(words)
    checkSingleChromosome(chromosome,limit,output_file)

if __name__ == "__main__":

    cutIntoSingleChromosome(input_path = "depth",
                            limit=0,
                            output_file="LoWCoverage")
