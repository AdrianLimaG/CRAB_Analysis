# CRAB Analysis Runner Documentation
_______________________________________

## Runnner Script for CRAB Pipeline

<br />

# CRAB_Analysis_Runner.py

- **CRAB_pipeline_worker()**
    - Class which runs the analysis
    - Upon initialization calls read_json to import necessary variables into class memory
    
- **run_CDCphoenix()**
    - Calls necessary functions to run Phoenix Analysis
    - Pushes results to SQL DB

- **run_pipeline()**
    - Calls necessary functions to run HomeBrew Analysis
    - Dumps run analysis into there corresponding [JSON](/data/run_data/) files in case of failure
    - Cleans up temporay files after

- **run_phylo_build()**
    - Calls necessary functions to build phylogenetic tree


- **clean_up_temp_files()**
    - Cleans up all temporay files

- **import_json()**
    - Function to read in run data from JSON files if run data exists


<br />
