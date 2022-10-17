from WF_0_Assembler.WF_0_Assembler_helper import run_assembler, sample_organizer, data_pre_processor


#runs assmebly for all samples, creates output dir, and return list of sample HSNs
def run_assembly(resource_path,path_to_samples,output_dir):

    #puts all of our samples in to dict with KEY HSN and [R1,R2]
    samp = sample_organizer(path_to_samples)
    #trimms reads, remove adapaters, remove poor quality reads
    samp = data_pre_processor(path_to_samples, samp)
    #running assembler on pre proccesed data
    run_assembler(resource_path,path_to_samples,samp,output_dir)

    return [*samp]

