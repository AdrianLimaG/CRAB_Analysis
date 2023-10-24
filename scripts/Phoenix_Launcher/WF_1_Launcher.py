import os
from Phoenix_Launcher.WF_1_helper import sample_organizer, run_phoniex_pipeline, Phoenix_create_dict
from WF_3_DB.WF_3_DB_push import run_DB_push


def WF_1_Launch_Phoniex(path_to_samples,sample_sheet_directory,rundate,ph_output_dir,path_to_p,kraken_p):
    #need to place phoniex in resources
    #command to run

    path_to_samples=ph_output_dir+"/sample_fastq/"+rundate
    sample_sheet_directory=sample_sheet_directory+"/"+rundate+".csv"

    if not(os.path.exists(ph_output_dir+"/Output/"+rundate)):
        os.mkdir(ph_output_dir+"/Output/"+rundate)
    
    ph_output_dir= ph_output_dir+"/Output/"+rundate

    p_hsn=sample_organizer(path_to_samples,sample_sheet_directory)
    print("starting ph")
    run_phoniex_pipeline(sample_sheet_directory,ph_output_dir,path_to_p,kraken_p)
    print("end ph")


    return p_hsn

def WF_2_PushDB_Phoniex(PH_OUT_PATH,run_date,cache_path,csv_path):

    mlst_type,amr_genes,assembly_metric = Phoenix_create_dict(PH_OUT_PATH,run_date)
    
#**** FIX ARM GENE THIONGGGGGG******
    run_DB_push(cache_path,[*mlst_type],mlst_type,amr_genes,assembly_metric,run_date,csv_path,True)




if __name__ == "__main__":

    WF_1_Launch_Phoniex("/home/ssh_user/WGS_Drive/Phoenix/sample_fastq/032323","/home/ssh_user/WGS_Drive/Phoenix/SampleSheet","032323","/home/ssh_user/WGS_Drive/Phoenix/Output","/home/ssh_user/Documents/GitHub/phoenix","/media/ssh_user/Data_Drive/Minikraken2DB")
    
