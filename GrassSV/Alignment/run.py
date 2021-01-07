import sys

from GrassSV.Alignment.load_alignments import load_alignments
from GrassSV.Alignment.contig_analysis import find_contig_patterns
from GrassSV.Alignment.translocation_detect import TranslocationFilter
from GrassSV.Alignment.pipeline import filter_inversions, \
    find_alignment_patterns, find_duplications
from GrassSV.Alignment.alignments import export_records, export_supporting_alignments



def run(contig_paths, output_folder_path='', export_patterns=False, export_support=False):
    [alignments,
     simple_contigs,
     complex_conigs] = load_alignments(contig_paths)

    alignment_patterns = find_alignment_patterns(alignments)
    contig_patterns = find_contig_patterns(simple_contigs)

    inversions_filtered = filter_inversions(contig_patterns.inversions)
    translocations, deletions, unused_breakpoints = TranslocationFilter()(deletions = contig_patterns.deletions,
                                                      translocation_breakpoints = contig_patterns.translocation_breakpoints)

    #find_duplications(contig_patterns.potential_duplications, alignment_patterns['others'])

    export_records(alignments, f"single_alignments.bed")
    export_records(simple_contigs, f"simple_contigs.bed")
    export_records(complex_conigs, f"complex_contigs.bed")

    export_records(contig_patterns.potential_duplications, f"{output_folder_path}/potential_duplications.bed")
    export_records(contig_patterns.deletions, f"{output_folder_path}/deletion_patterns.bed" )
    export_supporting_alignments(contig_patterns.deletions, f"{output_folder_path}/deletion_pattern_support.bed" )
    export_records(contig_patterns.translocation_breakpoints, f"{output_folder_path}/translocation_breakpoints.bed", name='')
    export_records(deletions, f"{output_folder_path}/deletions.bed" )
    export_records(translocations, f"{output_folder_path}/translocations.bed" )
    export_supporting_alignments(translocations, f"{output_folder_path}/translocations_support.bed")
    export_records(unused_breakpoints, f"{output_folder_path}/unused_translocation_breakpoints.bed", name='')
    pass
