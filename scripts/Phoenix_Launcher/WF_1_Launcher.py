
from Phoenix_Launcher.WF_1_helper import sample_organizer, run_phoniex_pipeline


def WF_1_Launch_Phoniex(path_to_samples,sample_sheet_directory,rundate,ph_output_dir,path_to_p,kraken_p):
    #need to place phoniex in resources
    #command to run

    p_hsn=sample_organizer(path_to_samples,sample_sheet_directory+"/"+rundate+".csv")

    run_phoniex_pipeline(sample_sheet_directory+"/"+rundate+".csv",ph_output_dir,path_to_p,kraken_p)



    return p_hsn
    