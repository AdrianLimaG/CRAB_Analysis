# Workflow 1 Script
_______________________________________

## Annoates genome and Multilocus sequence typing

<br />

# WF_1_Annotate.py

- **run_assembly()**
    - Calls run_mlst_typing, and run_prokka from helper file
    - Returns Dictionary of Multilocus sequence typing (MLST).

<br />

# WF_1_Annotate_helper.py

- **run_mlst_typing()**
    - Runs Multilocus sequence typing against consenus sequence
    - Return Dictionary of results

- **run_prokka()**
    - Annotates consense genome and produces gff files



<br />
