import sys

from GrassSV.Alignment.pattern import patterns_to_bed, supporting_alignments_to_bed
from GrassSV.Alignment.load_alignments import load_alignments
from GrassSV.Alignment.pipeline import find_contig_patterns, filter_inversions, \
    find_alignment_patterns, find_duplications


def run(contig_paths, output_folder_path='', export_patterns=False, export_supporting_alignments=False):
    [alignments,
     simple_contigs,
     complex_conigs] = load_alignments(contig_paths)

    alignment_patterns = find_alignment_patterns(alignments)
    contig_patterns = find_contig_patterns(simple_contigs)

    inversions_filtered = filter_inversions(contig_patterns["inversions"])
    find_duplications(contig_patterns["potential_duplications"], alignment_patterns["others"])

    if export_patterns:
        for name, patterns in alignment_patterns.items():
            output_path = output_folder_path + '/' + name + '_alignment_patterns.bed'
            patterns_to_bed(patterns, output_path)

        for name, patterns in contig_patterns.items():
            output_path = output_folder_path + '/' + name + '_contig_patterns.bed'
            patterns_to_bed(patterns, output_path)

    if export_supporting_alignments:
        for name, patterns in alignment_patterns.items():
            if name != 'others':
                output_path = output_folder_path + '/' + name + '_alignment_pattern_support.bed'
                supporting_alignments_to_bed(patterns, output_path)

        for name, patterns in contig_patterns.items():
            if name not in ['others', 'translocation breakpoints']:
                output_path = output_folder_path + '/' + name + '_contig_pattern_support.bed'
                supporting_alignments_to_bed(patterns, output_path)

    pass
