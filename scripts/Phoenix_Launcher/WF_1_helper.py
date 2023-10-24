import os
import subprocess
import csv

#function to pair reads put them into input for phoniex 

def sample_organizer(path_to_samples,output_file_path):
    sample_l= os.listdir(path_to_samples)
    phonex_samplesheet = open(output_file_path,"w+")
    w_file = csv.writer(phonex_samplesheet)
    header=["sample","fastq_1","fastq_2"]
    patient_hsn =[]
    w_file.writerow(header)

    for item in sample_l:
        hsn= item.split("-")[0]
        paired_end= item.split("_")
        #print(paired_end)
        if paired_end[3] == "R1":
            paired_end[3] = "R2"
            paired_end= "_".join(paired_end)
            w_file.writerow([hsn,path_to_samples+"/"+item,path_to_samples+"/"+paired_end])
            patient_hsn.append(hsn)
            sample_l.remove(paired_end)

    phonex_samplesheet.close()
    return patient_hsn

def run_phoniex_pipeline(phoniex_samplesheet,output_dir,path_to_phoenix,path_to_kraken):

    #command below
    #nextflow run $PATH_TO_INSTALL/phoenix/main.nf -entry PHOENIX -profile <singularity/docker/custom> --input <path_to_samplesheet.csv> --kraken2db $PATH_TO_DB
      #needs the conda env to be installed tho
    print("ph commaned")
    print(". $CONDA_PREFIX/home/ssh_user/mambaforge/etc/profile.d/conda.sh && conda activate nextflow && nextflow run "+path_to_phoenix+"/main.nf -profile docker -entry CDC_PHOENIX --input "+phoniex_samplesheet+" --kraken2db "+path_to_kraken+" --outdir "+output_dir)
    subprocess.run(". $CONDA_PREFIX/home/ssh_user/mambaforge/etc/profile.d/conda.sh && conda activate nextflow && nextflow run "+path_to_phoenix+"/main.nf -profile docker -entry CDC_PHOENIX --input "+phoniex_samplesheet+" --kraken2db "+path_to_kraken+" --outdir "+output_dir,shell=True)


def Phoenix_create_dict(path_to_output,rundate):
    #function will read in file container output and format it to be pushed to DB
    output_f = open(path_to_output+"/Output/"+rundate+"/Phoenix_Output_Report.tsv","r")
    lines = output_f.readlines()
    mlst_type = {}
    assembly_metrics={}
    amr_genes={}
    failed=[]
    #NEED TO LOOP THROUGH FILE AND EXTRACT
    #MLST
    i=1
    while i < len(lines):

        l = lines[i].split("\t")
        #print(l)
        if l[1] == "PASS":
            #create MLST DICT
            mlst_type[l[0]] = [l[0],l[8].split(" ")[0],l[16].split(",")[0][2:]]
            #create AMR GENE DICT
            amr_genes.update(parse_phoniex_AMR(l[0],path_to_output+"/Output/"+rundate+"/"+l[0]+"/AMRFinder/"+l[0]+"_all_genes.tsv"))
            #create ASSEMBLY METERE
            assembly_metrics[l[0]] = str(round(float(l[5].split(" ")[0]),3))

        else:
            #these fail wrtie them to a failed file
            failed.append(l)
        i+=1
    

    print("FAILED SAMPLES")
    print(failed)

    return mlst_type,amr_genes,assembly_metrics


def parse_phoniex_AMR(ID,path_to_AMR):
    amr_d={}
    amr_f = open(path_to_AMR,"r")
    amr_content = amr_f.readlines()
    for l in amr_content[1:] :
        g_lines=l.strip().split("\t")
        #GENE,%COVERAGE,%IDENTIT,DB_used,accession, product, resistan
        #print(g_lines)
        amr_d[ID+"_"+g_lines[5].strip()] = [ID,g_lines[5].strip(),g_lines[15],g_lines[16],"NA",g_lines[20],g_lines[6],g_lines[11] ]

   
    return amr_d


if __name__ == "__main__":
    pass
                            #path to samples                             path to sample_sheet_dir
    #sample_organizer("/home/ssh_user/WGS_Drive/Phoenix/sample_fastq/032323","/home/ssh_user/WGS_Drive/Phoenix/SampleSheet/")

    #run_phoniex_pipeline("/home/ssh_user/WGS_Drive/Phoenix/SampleSheet/032323.csv","")
            
