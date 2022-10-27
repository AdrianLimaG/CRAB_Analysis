import os
import subprocess
import json
#pre-running things
#trimmed adapter
#filter out low quality reads
#actually assemble


def data_pre_processor(path_to_reads,sample_d):
    #trimmed pair end reads
    #remove low quality reads
    os.mkdir(path_to_reads+"/fastp")
    for sample in [*sample_d]:
        #these should be seperated into there own folders
        #creating folder
        os.mkdir(path_to_reads+"/fastp/"+sample)
        
        subprocess.run("source activate CRAB && fastp -i "+path_to_reads+"/"+sample_d[sample][0]+" -o "+path_to_reads+"/fastp/"+sample+"/"+sample+"_R1.fastq.gz -I "+path_to_reads+"/"+sample_d[sample][1]+" -O "+path_to_reads+"/fastp/"+sample+"/"+sample+"_R2.fastq.gz -h "+path_to_reads+"/"+sample+"/"+sample+".html && source deactivate",shell=True)
        sample_d[sample][0]= sample+"_R1.fastq.gz"
        sample_d[sample][1]= sample+"_R2.fastq.gz"
 
    return sample_d

def run_assembler(resource_path,reads_path, sample_d, output_dir):
    #in here make a an output dir for each run with HSN being the folder name in the out dir
    for sample in sample_d:

        os.mkdir(output_dir+"/"+sample)
        subprocess.run("/usr/local/bin/python3 /Users/adrian/Desktop/SPAdes-3.15.5-Darwin/bin/spades.py --isolate -o"+output_dir+"/"+sample+" --pe1-1 "+reads_path+"/fastp/"+sample+"/"+sample_d[sample][0]+" --pe1-2 "+reads_path+"/fastp/"+sample+"/"+sample_d[sample][1], shell=True)
        #subprocess.run("python3 "+resource_path+"/resources/SPAdes-3.15.5-Linux/bin/spades.py --isolate -o "+output_dir+sample+" --pe1-1 "+reads_path+"/fastp/"+sample+"/"+sample_d[sample][0]+" --pe1-2 "+reads_path+"/fastp/"+sample+"/"+sample_d[sample][1], shell=True)
    


#function to pair reads put them in a dictonary maybe dump them into a json
def sample_organizer(path_to_samples):
    sample_l= os.listdir(path_to_samples)

    sample_dict ={}

    for item in sample_l:
        if item[-2:] == "gz":
            hsn= item.split("-")[0]
            if hsn not in sample_dict :
                paired_end= item.split("_")
            #print(paired_end)
                if paired_end[3] == "R1":
                    paired_end[3] = "R2"
                    paired_end= "_".join(paired_end)
                    sample_dict[hsn]=[item,paired_end]
            

    return sample_dict

 

 #produces an json which will be used to read in data
 #will but lineage data in resources
def check_assembly_qual(resource_path,path_to_fasta,qual_outputdir,samples):
    res={}
    #should also read in json file and store data
    for sample in samples:
        
        subprocess.run("source activate CRAB && busco -i "+path_to_fasta+"/"+sample+"/scaffolds.fasta -l "+resource_path+"/resources/busco/bacteria_odb10/ -o "+sample+"_busco --out_path "+qual_outputdir+" -m genome --offline && source deactivate", shell=True)
        
        #reading in json for stats
        temp = open(qual_outputdir+"/"+sample+"_busco"+"/short_summary.specific.bacteria_odb10."+sample+"_busco.json","r")
        sample_buso_res= json.load(temp)
        res[sample]=sample_buso_res["results"]["one_line_summary"]
      
    return res


if __name__ == "__main__":
    print(sample_organizer("/home/ks_khel/Desktop/CRAB_DATA/062422"))
