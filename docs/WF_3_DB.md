# Workflow 3 Script
_______________________________________

## Pushes results and demographical information to SQL Database

<br />

#WF_3_DB_push.py

- **run_DB_push()**
    - Calls demographics_import class from helper file
    - Runs functions to create pandas DF and pushes DF to DB

<br />

#WF_3_helper.py

- **get_lims_demographics()**
    - Uses samples IDs to pull demographical information from Horizon

- **format_lims_df()**
    - Formats dataframe from LIMS system to prepare for database push

- **create_metrics_df()**
    - Creates assembly metrics dataframe

- **create_mlst_df()**
    - Creates Multilocus sequence typing dataframe

- **create_genes_df()**
    - Creates antimicrobial resistance dataframe

- **merge_dfs()**
    - Merges LIMS, MLST, and Assembly metrics dataframe

- **format_dfs()**
    - Formats newly merged dataframe for database push

- **database_push()**
    - Pushes dataframe to database

- **database_push_genes()**
    - Pushes antimicrobial resistance dataframe to database


<br />
