from WF_3_5_SNP_Phylo.WF_3_5_helper import run_phylogenetic_tree, run_SNPCreation, join_paired_end_reads


def run_WF_3_5(path_to_trimmed_fastq, samples_list, path_to_shuffled_output, runDate, path_to_referance, SNP_output,out_put_tree_dir,path_to_assembled):

    join_paired_end_reads(path_to_trimmed_fastq, samples_list, path_to_shuffled_output)

    run_SNPCreation(path_to_shuffled_output,samples_list, SNP_output, runDate, path_to_referance)

    run_phylogenetic_tree(samples_list,path_to_assembled,path_to_referance,out_put_tree_dir)

