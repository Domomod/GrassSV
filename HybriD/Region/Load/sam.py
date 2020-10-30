class SamInstance:
    def __init__(self, fileContent: [str]):
        self.qname = fileContent[0]  # if type(qname) == str
        self.flag = int(fileContent[1])  # if type(flag) == int
        self.rname = fileContent[2]  # if type(rname) == str
        self.pos = int(fileContent[3])  # if type(pos) == int
        self.mapq = int(fileContent[4])  # if type(mapq) == int
        self.cigar = fileContent[5]  # if type(ciagr) == str
        self.rnext = fileContent[6]  # if type(rnext) == str
        self.pnext = int(fileContent[7])  # if type(pnext) == int
        self.tlen = int(fileContent[8])  # if type(tlen) == int
        self.seq = fileContent[9]  # if type(seq) == str
        self.qual = fileContent[10]  # if type(qual) == str
        if len(fileContent) > 11:
            self.atr = fileContent[11]
