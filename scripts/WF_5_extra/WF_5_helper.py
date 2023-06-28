from Bio import SeqIO
import subprocess
import os


def remove_reads(path_to_assembled,out_path,samples,runDate):
    if not(os.path.exists(out_path+"/"+runDate+"/fasta")):
        os.mkdir(out_path+"/"+runDate+"/fasta")
    
    out_path= out_path+"/"+runDate+"/fasta"

    for s in samples:
        output_f = open(out_path+"/"+s+".fasta")
        records = list(SeqIO.parse(path_to_assembled+"/"+runDate+"/"+s+"/scaffolds.fasta","fasta"))
        for r in records:
            if len(r.seq) > 200:
                SeqIO.write(r,output_f,"fasta")
        
        output_f.close()


#need to activate strain conda env
#one need to set up HDF5
def run_strain_analysis(samples,path_to_db,path_to_fastq,path_to_output,runDate):
    #create temp folder
    if not(os.path.exists(path_to_output+"/"+runDate+"/"+"strain_temp")):
        os.mkdir(path_to_output+"/"+runDate+"/"+"strain_temp")

    path_to_output=path_to_output+"/"+runDate+"/"+"strain_temp"
    #create hdf5 file

    for s in samples:
        #straingst kmerize -k 23 -o patient1.hdf5     patient1.1.fastq.gz patient1.2.fastq.gz
        subprocess.run(". $CONDA_PREFIX/home/ssh_user/mambaforge/etc/profile.d/conda.sh && conda activate STRAIN && straingst kmerize -k 23 -o "+path_to_output+"/"+s+".hdf5 "+path_to_fastq+"/"+runDate+"/"+s+"/"+s+"_R1_fp.fastq.gz "+path_to_fastq+"/"+runDate+"/"+s+"/"+s+"_R2_fp.fastq.gz",shell=True)
        
        
        subprocess.run(". $CONDA_PREFIX/home/ssh_user/mambaforge/etc/profile.d/conda.sh && conda activate STRAIN && straingst run -o "+path_to_output+"/"+s+".tsv "+path_to_db+" "+path_to_output+"/"+s+".hdf5",shell=True)

    #run 
    return path_to_output

#need to open text files to read
def read_strain(path_to_strains,samples,rundate):
    strain_info={}
    csv_out = "/".join(path_to_strains.split("/")[:-1])

    csv_f = open(csv_out+"/"+rundate+"_strainInfo.tsv","w+")

    for samp in samples:
        temp = open(path_to_strains+"/"+samp+".strains.tsv","r+")
        lines = temp.readlines()

        #should just write this to a csv file
        csv_f.write(samp+"\t"+lines[1].split("\t")[1])        
        strain_info[samp] = lines[1].split("\t")[1]
    
    csv_f.close()
    return strain_info







if __name__ == "__main__":
    pass
    #print(read_strain("/home//Desktop",["2281793TEST"]))

    #remove_reads

