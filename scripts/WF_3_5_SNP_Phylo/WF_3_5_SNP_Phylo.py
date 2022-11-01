from WF_3_5_SNP_Phylo.WF_3_5_helper import  run_SNPCreation, join_paired_end_reads, run_docker


def run_WF_3_5(path_to_trimmed_fastq, samples_list, path_to_shuffled_output, runDate, path_to_referance, SNP_output):

    #run docker to create snp and phylo tree
    run_docker(path_to_trimmed_fastq,samples_list,path_to_shuffled_output,runDate,SNP_output,path_to_referance)





