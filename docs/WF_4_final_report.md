# Workflow 4 Script
_______________________________________

## Build Final EPI Report

<br />

# WF_4_helper.py

- **run_create_PDF()**
    - Calls FPDF class to build PDF report
    
- **format_table_gene_data()**
    - Formats seperates OXA genes from other gene from main gene dictionary
    - Returns two dictionaries of resistance gene information

- **format_table_data()**
    - Formats all data to be printed on PDF
    - Return list of table data

- **create_phlyo_image()**
    - Calls mod_tree_text to create a modifiy phylogenetic tree file.
    - Takes new newick tree files and creates png file.

- **load_matrix()**
    - Reads in snp matrix data.

- **creat_snp_image()**
    - Creates a png image using snp matrix data.

- **mod_tree_text()**
    - Reads in phylogenetic tree and trims branch data to readability when converted to image.


<br />

