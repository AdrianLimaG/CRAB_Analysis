from WF_5_extra.WF_5_helper import remove_reads, run_strain_analysis, read_strain



def run_WF_5 (sample_l,runD, path_to_fastqs, path_to_results, path_to_strainDB):

    remove_reads(path_to_fastqs,path_to_results,sample_l,runD)

    out_p = run_strain_analysis(sample_l,path_to_strainDB,path_to_fastqs,path_to_results,runD)

    strains=read_strain(out_p,sample_l)

    return strains
    