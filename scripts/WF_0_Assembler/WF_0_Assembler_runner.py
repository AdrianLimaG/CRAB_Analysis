from WF_0_Assembler.WF_0_Assembler_helper import run_assembler, sample_organizer, data_pre_processor, check_assembly_qual


#runs assmebly for all samples, creates output dir, and return list of sample HSNs
def run_assembly(resource_path,path_to_samples,output_dir,busco_output_dir):

    #puts all of our samples in to dict with KEY HSN and [R1,R2]
    samp = sample_organizer(path_to_samples)
    #trimms reads, remove adapaters, remove poor quality reads
    samp = data_pre_processor(path_to_samples, samp)
    #running assembler on pre proccesed data
    run_assembler(resource_path,path_to_samples,samp,output_dir)

    #could move this to DB push to save ram memory
    assembly_stats=check_assembly_qual(resource_path,path_to_samples,busco_output_dir,[*samp])


    return [*samp]

