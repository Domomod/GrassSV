
def find_translocation(deletions, translocation_breakpoints):
    translocations=[]
    translocation_breakpoints.sort(key=lambda breakpoint: (breakpoint.aligments[0].chromosome))
    deletions.sort(key=lambda deletion: (deletion.chromosome))
    startpoint=0
    lastused=0
    for deletioniteration in range (len(deletions)):
        if deletioniteration==0 or deletions[deletioniteration-1].chromosome:
            lastused=startpoint
            while translocation_breakpoints[lastused].aligments[0].chromosome==deletions[deletioniteration].chromosome:
                if (deletions[deletioniteration].start < translocation_breakpoints[lastused].aligments[0].aligment_start and deletions[deletioniteration].end > translocation_breakpoints[lastused].aligments[0].aligment_start):
                    translocations.append(Tuple(deletions[deletioniteration], translocation_breakpoints[lastused]))
                if (deletions[deletioniteration].start < translocation_breakpoints[lastused].aligments[0].aligment_end and deletions[deletioniteration].end > translocation_breakpoints[lastused].aligments[0].aligment_end):
                    translocations.append(Tuple(deletions[deletioniteration], translocation_breakpoints[lastused]))
                lastused+=1
        else: #new chromosome
            startpoint=lastused
            while translocation_breakpoints[lastused].aligments[0].chromosome==deletions[deletioniteration].chromosome:
                if (deletions[deletioniteration].start < translocation_breakpoints[lastused].aligments[0].aligment_start and deletions[deletioniteration].end > translocation_breakpoints[lastused].aligments[0].aligment_start):
                    translocations.append(Tuple(deletions[deletioniteration], translocation_breakpoints[lastused]))
                if (deletions[deletioniteration].start < translocation_breakpoints[lastused].aligments[0].aligment_end and deletions[deletioniteration].end > translocation_breakpoints[lastused].aligments[0].aligment_end):
                    translocations.append(Tuple(deletions[deletioniteration], translocation_breakpoints[lastused]))
                lastused+=1
    translocation_breakpoints.sort(key=lambda breakpoint:(breakpoint.aligments[1].chromosome))
    startpoint=0
    lastused=0
    for deletioniteration in range (len(deletions)):
        if deletioniteration==0 or deletions[deletioniteration-1].chromosome:
            lastused=startpoint
            while translocation_breakpoints[lastused].aligments[1].chromosome==deletions[deletioniteration].chromosome:
                if (deletions[deletioniteration].start < translocation_breakpoints[lastused].aligments[1].aligment_start and deletions[deletioniteration].end > translocation_breakpoints[lastused].aligments[0].aligment_start):
                    translocations.append(Tuple(deletions[deletioniteration], translocation_breakpoints[lastused]))
                if (deletions[deletioniteration].start < translocation_breakpoints[lastused].aligments[1].aligment_end and deletions[deletioniteration].end > translocation_breakpoints[lastused].aligments[0].aligment_end):
                    translocations.append(Tuple(deletions[deletioniteration], translocation_breakpoints[lastused]))
                lastused+=1
        else: #new chromosome
            startpoint=lastused
            while translocation_breakpoints[lastused].aligments[1].chromosome==deletions[deletioniteration].chromosome:
                if (deletions[deletioniteration].start < translocation_breakpoints[lastused].aligments[1].aligment_start and deletions[deletioniteration].end > translocation_breakpoints[lastused].aligments[0].aligment_start):
                    translocations.append(Tuple(deletions[deletioniteration], translocation_breakpoints[lastused]))
                if (deletions[deletioniteration].start < translocation_breakpoints[lastused].aligments[1].aligment_end and deletions[deletioniteration].end > translocation_breakpoints[lastused].aligments[0].aligment_end):
                    translocations.append(Tuple(deletions[deletioniteration], translocation_breakpoints[lastused]))
                lastused+=1
    return translocations
