
from WF_1_Phoenix_Launcher.WF_1_helper import sample_organizer, run_phoniex_pipeline


def WF_1_Launch_Phoniex(path_to_samples,output_directoty):
    #need to place phoniex in resources
    #command to run

    p_hsn=sample_organizer(path_to_samples,"something")

    return p_hsn
    