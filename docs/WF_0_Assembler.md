# Workflow 0 Script
_______________________________________

## Prepares raw reads and assembles genome

<br />

# WF_0_Assembler_runner.py

- **run_assembly()**
    - Calls run_assembler, sample_organizer, data_pre_processor, and check_assembly_qual from helper file
    - Returns list of sample id's and assembly metrics

<br />

# WF_0_Assembler_helper.py

- **sample_organizer()**
    - Function finds reads and organizes them into a dict
    - Returns Dictionary of all{SampleID: \[R1,R2\]}

- **data_pre_processor()**
    - Removes low quality reads and trimmes reads
    - Returns {SampleID: \[R1,R2\]}} for new fastq files

- **run_assembler()**
    - Runs Spades assembly 



<br />
