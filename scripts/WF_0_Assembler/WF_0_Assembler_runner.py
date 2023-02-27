from WF_0_Assembler.WF_0_Assembler_helper import run_assembler, sample_organizer, data_pre_processor, check_assembly_qual


#runs assmebly for all samples, creates output dir, and return list of sample HSNs
def run_assembly(resource_path,path_to_samples,output_dir,busco_output_dir,runD):
    
    #puts all of our samples in to dict with KEY HSN and [R1,R2]
    samp = sample_organizer(path_to_samples)
    print("Organiizing Complete")

    #trimms reads, remove adapaters, remove poor quality reads
    samp = data_pre_processor(path_to_samples, samp)
    
    #samp = { '2278019': ['2278019_R1.fastq.gz', '2278019_R2.fastq.gz'], '2278016': ['2278016_R1.fastq.gz', '2278016_R2.fastq.gz'], '2281037': ['2281037_R1.fastq.gz', '2281037_R2.fastq.gz'], '2281793': ['2281793_R1.fastq.gz', '2281793_R2.fastq.gz']}
    print("PreProcessing Data Complete")

    #running assembler on pre proccesed data
    run_assembler(resource_path,path_to_samples,samp,output_dir,runD)
    print("SPADES Assembly complete")

    #could move this to DB push to save ram memory
    assembly_stats=check_assembly_qual(resource_path,output_dir,busco_output_dir,[*samp],runD)
    print("Busco Completes, return values")
    
    return [*samp], assembly_stats

