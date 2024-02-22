import os
from Phoenix_Launcher.WF_1_helper import sample_organizer, run_phoenix_pipeline, Phoenix_create_dict
from WF_3_DB.WF_3_DB_push import run_DB_push
from WF_4_CreateReport.WF_4_helper import CDC_PDF_Report
 
def WF_1_Launch_Phoenix(path_to_samples,sample_sheet_directory,rundate,ph_output_dir,path_to_p,kraken_p):
    #need to place Phoenix in resources
    #command to run

    path_to_samples=ph_output_dir+"/sample_fastq/"+rundate
    sample_sheet_directory=sample_sheet_directory+"/"+rundate+".csv"

    if not(os.path.exists(ph_output_dir+"/Output/"+rundate)):
        os.mkdir(ph_output_dir+"/Output/"+rundate)
    
    ph_output_dir= ph_output_dir+"/Output/"+rundate

    p_hsn=sample_organizer(path_to_samples,sample_sheet_directory)
    print("starting ph")
    run_phoenix_pipeline(sample_sheet_directory,ph_output_dir,path_to_p,kraken_p)
    print("end ph")


    return p_hsn

def WF_2_PushDB_Phoenix(PH_OUT_PATH,run_date,cache_path,csv_path,pdf_path,resource_p,create_report):

    mlst_type,amr_genes,assembly_metric = Phoenix_create_dict(PH_OUT_PATH,run_date)
    
#**** FIX ARM GENE THIONGGGGGG******
    #run_DB_push(cache_path,[*mlst_type],mlst_type,amr_genes,assembly_metric,run_date,csv_path,True)

    if create_report:
#create Report
        CDC_PDF_Report([*mlst_type],run_date,pdf_path,resource_p,amr_genes,mlst_type)

#CDC_PDF_Report(samples,run_date,output_pdf_dir,resource_path,found_genes, mlst_dict)
def WF_3_create_report(samps,run_d,pdf_path,resource_p,genes,mlst_d):
    pass




if __name__ == "__main__":

    WF_1_Launch_Phoenix("/home/ssh_user/WGS_Drive/Phoenix/sample_fastq/032323","/home/ssh_user/WGS_Drive/Phoenix/SampleSheet","032323","/home/ssh_user/WGS_Drive/Phoenix/Output","/home/ssh_user/Documents/GitHub/phoenix","/media/ssh_user/Data_Drive/Minikraken2DB")
    
