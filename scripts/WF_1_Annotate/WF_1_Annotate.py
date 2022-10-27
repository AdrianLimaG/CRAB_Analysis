from WF_1_Annotate.WF_1_helper import run_mlst_typing, run_prokka


def run_annotate(path_to_assembled,prokka_outputdir,sample_hsn):

    mlst_typing = run_mlst_typing(path_to_assembled,sample_hsn)
    
    run_prokka(path_to_assembled,prokka_outputdir,sample_hsn)

    return mlst_typing

