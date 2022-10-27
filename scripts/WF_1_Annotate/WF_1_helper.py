import os
import subprocess





def run_mlst_typing(path_to_contigs,samples):
    typing={}
    for samp in samples:
        temp=subprocess.run("source activate CRAB && mlst "+path_to_contigs+"/"+samp+"/scaffolds.fasta && source deactivate",capture_output=True, text=True,shell=True)
        typing[samp]=[samp]+temp.stdout.strip().split("\t")[1:3]

    # need to figure out how to store the data json?
    #keep it in a var until i wirte to DB
    return typing

def run_prokka(path_to_contigs,output_dir,samples):

    for samp in samples:
        
        subprocess.run("source activate CRAB && prokka --genus Acinetobacter --species baumannii "+path_to_contigs+"/"+samp+"/scaffolds.fasta --outdir "+output_dir+"/"+samp+" && source deactivate",shell=True)
    


if __name__ == "__main__":
    print(run_mlst_typing("/Users/adrian/Desktop/CRAB_OUT",['2296669_manualy']))
    #Desktop/CRAB_OUT/2296669_manualy/scaffolds.fasta 
    pass
