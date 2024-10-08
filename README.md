# GrassSV
GrassSV is a command-line interface (CLI) tool used for detecting structural variants in genomic data.


```
usage: GrassSV.py [-h] {rsvsim2bed,find_sv,find_roi,roi_statistics,quast2bed,
                         filter_reads,slurm_dispatch,find_hdr,run_standalone,utils} ...

positional arguments:
  {rsvsim2bed,find_sv,find_roi,roi_statistics,quast2bed,filter_reads,slurm_dispatch,find_hdr,run_standalone,
  utils}
                        GrassSV consits of multiple scripts:
    rsvsim2bed          converts sequences from rsvsims's csv format to bed
    find_sv             finds structural variations based on contig's alignments
    find_roi            finds regions of intrest based on mapping coverage
    roi_statistics      confronts found regions with generated mutations
    quast2bed           converts sequences from quast tsv format to bed
    filter_reads        Filter reads by regions of interest
    slurm_dispatch
    find_hdr            finds regions of high depth coverage
    run_standalone      Runs GrassSV pipeline in a single run
    utils               Utilities [csv2bed, sv_check]
```

# Running without Slurm

To detect structural variants (SVs) using GrassSV, follow these steps:

1. Map your reads to the reference genome and calculate the depth of coverage.
2. Run GrassSV find_roi – this will identify regions where SV breakpoints are suspected.
3. Run GrassSV filter_reads – this will filter out reads that are unlikely to provide information about SVs.
4. Assemble the filtered reads into contigs (e.g., using the ALGA assembler).
5. Map the filtered contigs to the reference genome.
6. Run GrassSV find_sv – this will produce SV calls with annotated variant types.

## Run steps 1-6 with GrassSV.py run_standalone [Recommmended] 
Steps 1-6 can be simplified as one call.
`GrassSV.py run_standalone -g ${CX_REFERENCE} -i ${CX_INDEX} -l ${CX_REFERENCE_LENGTH} -r ${CX_READS_1} -R ${CX_READS_2}`

With `CX_REFERENCE` leading to reference genome file (.fai), `CX_INDEX` leading to genoe index file, `CX_REFERENCE_LENGTH` leading to genome lengths file. `CX_READS_1` and `CX_READS_1` should lead to FASTQ (.fq) formated reads. 

The script is available in `origin/docker` branch of this repository.

### GrassSV.py run_standalone Script Requrements
ALGA, samtools(1.6.0), bowtie1(1.0.0), bowtie2(2.2.3), gcc(7.4.0), quast(5.0.2) 

# Running with SLURM
Running GrassSV is simpler with SLURM, only one command is needed. 

```
usage: GrassSV.py slurm_dispatch [-h] 
[-S {GEN_MUTATION,RUN_ART,CALC_DEPTH,EXTRACT\_READS,RUN\_GRASS,RUN_ALGA,RUN_QUAST,
      RUN_QUAST_ALGA,NONE}] 
[-G {none,dup,del,tra,ins,inv,all}] -g path -o path

optional arguments:
  -h, --help            show this help message and exit
  -S {GEN_MUTATION,RUN_ART,CALC_DEPTH,EXTRACT_READS,RUN_GRASS,RUN_ALGA,RUN\_QUAST,
       RUN_QUAST_ALGA,NONE}
                        [Optional] Select the job to start from:
                        [GEN_MUTATION,RUN_ART,CALC_DEPTH,EXTRACT_READS,RUN_GRASS,RUN_ALGA,
                         RUN_QUAST,RUN_QUAST_ALGA,NONE]. 
                        Defaults to CALC_DEPTH.
  -G {none,dup,del,tra,ins,inv,all}
                        [Optional] You may generate mutations using our fastaDNA generator. 
                        To do so specify what mutations do you want to generate: 
                        [none, dup, del, tra, ins, inv, all]
  -g path, --genome path
                        The genome file that will be copied to output folder.
  -o path, --output path
                        The output folder where GrassSv output will be generated. 
                        Do not store multiple outputs in the same folder as they would overwrite eachother.
```

To run GrassSV on your data type:
```
GrassSV.py slurm_dispatch -S CALC_DEPTH
```

# Benchmarking on a test dataset
GrassSV was tested against following SV Callers: Pindel, Lumpy and GRIDSS. Benchmark code alongside benchmarking data can be found at GrassBenchmark repository: https://github.com/Domomod/GrassBenchmark.
