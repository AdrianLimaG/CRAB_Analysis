import subprocess
import os


def join_paired_end_reads(path_to_fastq,samples,path_to_shuffled):
    #path to fastq should put us in the fastp folder created with each sample 
    #path_to_allreads/fastp/sample
    docker_string=""

    for sample in samples:

        docker_string+="cd /data/FASTQ/"+sample+" &&  shuffleSplitReads.pl --numcpus 8 "+sample+"_R* -o /data/CRAB/ && "

    #subprocess.run("docker run -v "+path_to_shuffled+":/data/CRAB -v "+path_to_fastq+"/fastp::/data/FASTQ staphb/lyveset:1.1.4f /bin/bash -c '"+docker_string+"'",shell =True)
    print("docker run -v "+path_to_shuffled+":/data/CRAB -v "+path_to_fastq+"/fastp:/data/FASTQ staphb/lyveset:1.1.4f /bin/bash -c '"+docker_string+"'")
   
def run_SNPCreation(path_to_shuffled_reads,samples,output_mount,run_date,path_to_referance):
    docker_string="set_manage.pl --create /data/Output/"+run_date+" && set_manage.pl /data/Output/"+run_date+" --change-reference /data/referance/GCF_008632635.1_ASM863263v1_referance_genome.fna && "

    for sample in samples:
        docker_string+="set_manage.pl --add-reads /data/Output/"+sample+".fastq.gz && "

    #subprocess.run("docker run -v "+path_to_shuffled_reads+":/data/CRAB -v "+path_to_referance+":/data/referance -v "+output_mount+":/data/Output staphb/lyveset:1.1.4f /bin/bash -c '"+docker_string+"launch_set.pl /data/Output"+run_date+"'",shell=True)
    print("docker run -v "+path_to_shuffled_reads+":/data/CRAB -v "+path_to_referance+":/data/referance -v "+output_mount+":/data/Output staphb/lyveset:1.1.4f /bin/bash -c '"+docker_string+"launch_set.pl --numcpus 8 /data/Output"+run_date+"'")


def create_heatmap():
    pass


def run_phylogenetic_tree():

    pass