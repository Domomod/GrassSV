import sys

from HybriD.Detection.Pattern import patternsAsBed
from HybriD.Detection.QuastLoad import loadQuastContigs
from HybriD.Detection.DetectionPipeline import analyzeTwoAlignmentsContigs, analyzeInversions, \
    analyzeOneAlignmentContigs, searchForDuplications

if __name__ == "__main__":
    [contigsOneAlignment,
     contigsTwoAlignments,
     contigsManyAlignments] = loadQuastContigs(sys.argv[1])

    patternsOneAlignment = analyzeOneAlignmentContigs(contigsOneAlignment)
    patternsTwoAlignments = analyzeTwoAlignmentsContigs(contigsTwoAlignments)

    inversionsFiltered = analyzeInversions(patternsTwoAlignments["inversions"])
    searchForDuplications(patternsTwoAlignments["potential_duplications"], patternsOneAlignment["others"])
    pass