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

    alignment_insertions = alignment_patterns["insertions"]
    contig_insertions = contig_patterns.insertions
    insertions = contig_insertions + alignment_insertions

    inversions_filtered = filter_inversions(contig_patterns.inversions)

    translocations, deletions, unused_breakpoints, duplications \
        = TranslocationFilter()(deletions=contig_patterns.deletions,
                                translocation_breakpoints=contig_patterns.translocation_breakpoints,
                                duplications=contig_patterns.potential_duplications)

    # find_duplications(contig_patterns.potential_duplications, alignment_patterns['others'])


    #Raport
    export_records(contig_insertions, f"{output_folder_path}/detectedSVs/insertions.bed")
    export_records(alignment_insertions, f"{output_folder_path}/detectedSVs/insertions_low_confidence.bed")
    export_records(inversions_filtered, f"{output_folder_path}/detectedSVs/inversions.bed")
    export_records(deletions, f"{output_folder_path}/detectedSVs/deletions.bed")
    #export_records(duplications, f"{output_folder_path}/detectedSVs/duplications.bed")
    export_records(translocations, f"{output_folder_path}/detectedSVs/translocations.bed")

    #For debug
    if True or export_support:
        export_supporting_alignments(contig_insertions, f"{output_folder_path}/supportForSVs/insertions_support.bed")
        export_supporting_alignments(alignment_insertions, f"{output_folder_path}/supportForSVs/insertions_low_confidence_support.bed")
        export_supporting_alignments(inversions_filtered, f"{output_folder_path}/supportForSVs/inversions_support.bed")
        export_supporting_alignments(deletions, f"{output_folder_path}/supportForSVs/deletions_support.bed")
        #export_supporting_alignments(duplications, f"{output_folder_path}/supportForSVs/duplications_support.bed")
        export_supporting_alignments(translocations, f"{output_folder_path}/supportForSVs/translocations_support.bed")

    if True or  export_patterns:
        export_records(contig_patterns.potential_duplications, f"{output_folder_path}/patterns/duplication_patterns.bed")
        export_records(contig_patterns.deletions, f"{output_folder_path}/patterns/deletion_patterns.bed")
        export_records(contig_patterns.inversions, f"{output_folder_path}/patterns/inversion_patterns.bed")
        export_records(contig_patterns.translocation_breakpoints, f"{output_folder_path}/patterns/translocation_breakpoint_patterns.bed")
        export_records(contig_patterns.insertions, f"{output_folder_path}/patterns/contig_insertion_patterns.bed")
        export_records(alignment_patterns["insertions"], f"{output_folder_path}/patterns/alignment_insertions_patterns.bed")
