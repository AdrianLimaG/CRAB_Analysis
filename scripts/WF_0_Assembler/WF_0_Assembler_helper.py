import os
import subprocess

#pre-running things
#trimmed adapter
#filter out low quality reads
#actually assemble


def data_pre_processor(path_to_reads,sample_d):
    #trimmed pair end reads
    #remove low quality reads
    for sample in [*sample_d]:
        subprocess.run("source activate CRAB && fastp -i "+path_to_reads+"/"+sample+"/"+sample_d[sample][0]+" -o "+path_to_reads+"/"+sample+"/"+sample+"_R1.fastq.gz -I "+path_to_reads+"/"+sample+"/"+sample_d[sample][1]+" -O "+path_to_reads+"/"+sample+"/"+sample+"_R2.fastq.gz -h "+path_to_reads+"/"+sample+"/"+sample+".html && source deactivate",shell=True)
        sample_d[sample][0]= sample+"_R1.fastq.gz"
        sample_d[sample][1]= sample+"_R2.fastq.gz"
    #fastp -i Desktop/CRAB_DATA/071422/2296669-KS-M4269-220714_S5_L001_R1_001.fastq.gz -o Desktop/CRAB_DATA/2296669_R1_fastp.fastq.gz -I Desktop/CRAB_DATA/071422/2296669-KS-M4269-220714_S5_L001_R2_001.fastq.gz -O Desktop/CRAB_DATA/2296669_R2_fastp.fastq.gz -h Desktop/CRAB_DATA/229669.html

    return sample_d

def run_assembler(resource_path,reads_path, sample_d, output_dir):

   
    #in here make a an output dir for each run with HSN being the folder name in the out dir
    for sample in sample_d:

        os.mkdir(output_dir+sample)

        subprocess.run("python3 "+resource_path+"/resources/SPAdes-3.15.5-Linux/bin/spades.py -o "+output_dir+sample+" --pe1-1 "+reads_path+"/"+sample_d[sample][0]+" --pe1-2 "+reads_path+"/"+sample_d[sample][1], shell=True)
    
#python3 spades.py -o /home/ks_khel/Desktop/CRAB_OUT/ --pe1-1 /home/ks_khel/Desktop/CRAB_DATA/COPY/2296669-KS-M4269-220714_S5_L001_R1_001.fastq.gz --pe1-2 /home/ks_khel/Desktop/CRAB_DATA/COPY/2296669-KS-M4269-220714_S5_L001_R2_001.fastq.gz 

#function to pair reads put them in a dictonary maybe dump them into a json
def sample_organizer(path_to_samples):
    sample_l= os.listdir(path_to_samples)

    sample_dict ={}

    for item in sample_l:
        hsn= item.split("-")[0]
        paired_end= item.split("_")
        if paired_end[3] == "R1":
            paired_end[3] = "R2"
            paired_end= "_".join(paired_end)
            sample_l.remove(paired_end)
            paired_end= "_".join(paired_end)
            sample_dict[hsn]=[item,paired_end]
            sample_l.remove(paired_end)

    return sample_dict

if __name__ == "__main__":
    print(sample_organizer("/home/ks_khel/Desktop/CRAB_DATA/062422"))
