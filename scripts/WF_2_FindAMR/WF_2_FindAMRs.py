from WF_2_FindAMR.WF_2_helper import run_AMR, parse_AMR



def find_AMR_genes(sample_list,path_to_samples,amr_output_dir):

    run_AMR(path_to_samples,sample_list,amr_output_dir)

    parsed_data = parse_AMR(amr_output_dir,sample_list)

    return parsed_data