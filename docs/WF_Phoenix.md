# Phoenix Workflow Script
_______________________________________

## Wrapper Script to Run Phoenix

<br />

# WF_1_Launcher.py

- **WF_1_Launch_Phoenix**
    - Creates output folder
    - Creates samplesheet needed for Phoenix
    - Runs Phoenix

- **WF_2_PushDB_phoenix**
    - Calls Phoenix_create_dict to format Phoenix output into DICT format for DB push
    - Pushes results to SQL DB

<br />

# WF_1_helper.py

- **sample_organizer()**
    - Creates samples sheet for Phoenix
    - Returns sample IDs for down stream use
    
- **run_phoenix_pipeline()**
    - Runs Phoenix

- **Phoenix_create_dict()**
    - Creates dictionaries for Phoneix output files
    - Calls parse_phoenix_AMR to create AMR_gene dict

- **parse_phoenix_AMR()**
    - Create a dictionary of AMR genes for a given sample 


<br />