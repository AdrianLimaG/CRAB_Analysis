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
        print(paired_end)
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
    subprocess.run(". $CONDA_PREFIX/home/ssh_user/mambaforge/etc/profile.d/conda.sh && conda activate nextflow && nextflow run "+path_to_phoenix+"/phoenix/main.nf -entry PHOENIX --input "+phoniex_samplesheet+" --kraken2db "+path_to_kraken+" --outdir "+output_dir,shell=True)



if __name__ == "__main__":
    sample_organizer("/Users/adrian/Desktop/CRAB_DATA/0714222","/Users/adrian/Desktop/CRAB_DATA/0714222_samplesheet.csv")