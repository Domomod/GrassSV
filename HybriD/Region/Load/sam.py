class SamInstance:
    def __init__(self, qname, flag, rname, pos, mapq, cigar, rnext, pnext, tlen, seq, qual, atr):
        self.qname = qname  # if type(qname) == str
        self.flag = int(flag)  # if type(flag) == int
        self.rname = rname  # if type(rname) == str
        self.pos = int(pos)  # if type(pos) == int
        self.mapq = int(mapq)  # if type(mapq) == int
        self.cigar = cigar  # if type(ciagr) == str
        self.rnext = rnext  # if type(rnext) == str
        self.pnext = int(pnext)  # if type(pnext) == int
        self.tlen = int(tlen)  # if type(tlen) == int
        self.seq = seq  # if type(seq) == str
        self.qual = qual  # if type(qual) == str
        self.atr = atr
