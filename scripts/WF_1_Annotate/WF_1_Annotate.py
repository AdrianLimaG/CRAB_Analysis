from WF_1_Annotate.WF_1_helper import run_mlst_typing, run_prokka

#from WF_0_Assembler.WF_0_Assembler_helper import run_assembler, sample_organizer, data_pre_processor

def run_annotate(path_to_assembled,prokka_outputdir,sample_hsn):

    mlst_typing = run_mlst_typing(path_to_assembled,sample_hsn)

    run_prokka(path_to_assembled,prokka_outputdir,sample_hsn)

    return mlst_typing

