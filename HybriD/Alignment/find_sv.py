import sys

from HybriD.Alignment.pattern import patterns_to_bed
from HybriD.Alignment.load_alignments import load_alignments
from HybriD.Alignment.pipeline import find_contig_patterns, filter_inversions, \
    find_alignment_patterns, find_duplications

def run(contig_paths):
    [alignments,
     simple_contigs,
     complex_conigs] = load_alignments(contig_paths)

    alignment_patterns = find_alignment_patterns(alignments)
    contig_patterns = find_contig_patterns(simple_contigs)

    inversions_filtered = filter_inversions(contig_patterns["inversions"])
    find_duplications(contig_patterns["potential_duplications"], alignment_patterns["others"])
    pass