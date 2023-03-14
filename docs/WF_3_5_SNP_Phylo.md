# Workflow 3.5 Script
_______________________________________

## Creates SNP heatmap and Phylogenetic Tree

<br />

#WF_3_5_SNP_Phylo.py

- **frun_WF_3_5()**
    - Calls run_docker, parse_AMR from helper file

<br />

#WF_3_5_helper.py

- **run_docker()**
    - Calls on join_paired_end_reads and run_SNPCreation to create docker commands
    - Runs staphb/lyvese docker to create SNP heat map creation and build Phylogentic tree
    
- **join_paired_end_reads()**
    - Creates docker command to shuffle paired-end reads
    - Return docker command string

- **run_SNPCreation()**
    - Creates docker command to run SNP heat map creation and build Phylogentic tree 
    - Return docker command string


<br />
