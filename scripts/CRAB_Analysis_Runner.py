#CRAB Pipeline
from WF_0_Assembler.WF_0_Assembler_runner import run_assembly
from WF_1_Annotate.WF_1_Annotate import run_annotate
from WF_2_FindAMR.WF_2_FindAMRs import find_AMR_genes
from WF_3_DB.WF_3_DB_push import run_DB_push
from WF_3_5_SNP_Phylo.WF_3_5_SNP_Phylo import run_WF_3_5
from WF_4_CreateReport.WF_4_helper import run_create_PDF
import os
import sys
import json
import reader
#Main body of the scrip which will run the rest


class CRAB_pipeline_worker():

    def __init__(self, path_to_reads,sample_sheet_p, cache_path) :
        self.path_to_reads = path_to_reads
        self.sample_sheet_p = sample_sheet_p
        self.run_data = sample_sheet_p.split("/")[-1][:-4]

        demo_cahce= reader.read_json(cache_path+"/data/pipeline_variables.json")
        for item in [*demo_cahce] :
            setattr(self,item, demo_cahce[item])

    def run_pipeline(self):
        pass
        
            #WF_0
        #Fastq pre proccessing, runs SPADES assembler, RETURNS list of HSN
        sample_HSN , Assembly_stats = run_assembly(parent_dir_path,path_to_reads,assembly_output,busco_output)
        print("Assembly Done")

        sample_HSN =['2278019', '2278016', '2281037', '2281793']

        #WF_1
        #runs Prokka
        #runs MLST typing, RETURNS MLST TYPE in DICT {"HSH":[species,type, something, ...]} 
                                                    #{'2296669_manualy': ['2296669_manualy', 'abaumannii_2', '2']}
        mlst = run_annotate(assembly_output,prokka_output,sample_HSN)
        print("Annotation Done")
        print(mlst)

        #WF_2
        #Runs Abricate, converts the output to something to be pushed to DB
    
        found_genes = find_AMR_genes(sample_HSN,assembly_output,abricate_output)
        print("found AMR genes")
        #found_genes DICT {HSN:[GENE,%COV,%IDENT,DB_Used,Accession_Seq,Gene_Product,Resistance]}

        #WF_3 DB push
        #demographical push
        #gene and anti-micorable data
        #MLST typing 
        run_DB_push(parent_dir_path,sample_HSN,mlst,found_genes) #this one!!!!
        #run_DB_push("/Users/adrian/Documents/GitHub/CRAB_Analysis",['22222'],{"222222":["something"]},{'2296669': [ ['2296669', 'blaADC-30', '100.00', '100.00', 'ncbi', 'NG_048652.1', 'class C extended-spectrum beta-lactamase ADC-30', 'CEPHALOSPORIN'], ['2296669', 'tet(B)', '99.50', '100.00', 'ncbi', 'NG_048161.1', 'tetracycline efflux MFS transporter Tet(B)', 'TETRACYCLINE'], ['2296669', 'aph(6)-Id', '100.00', '100.00', 'ncbi', 'NG_047464.1', 'aminoglycoside O-phosphotransferase APH(6)-Id', 'STREPTOMYCIN'], ['2296669', 'aph(3'')-Ib', '98.31', '99.88', 'ncbi', 'NG_056002.2', 'aminoglycoside O-phosphotransferase APH(3'')-Ib', 'STREPTOMYCIN'], ['2296669', 'blaOXA-66', '100.00', '100.00', 'ncbi', 'NG_049806.1', 'OXA-51 family carbapenem-hydrolyzing class D beta-lactamase OXA-66', 'CARBAPENEM'], ['2296669', 'sul2', '100.00', '100.00', 'ncbi', 'NG_051852.1', 'sulfonamide-resistant dihydropteroate synthase Sul2', 'SULFONAMIDE'], ['2296669', 'ant(3'')-IIa', '100.00', '98.61', 'ncbi', 'NG_054646.1', 'aminoglycoside nucleotidyltransferase ANT(3'')-IIa', 'SPECTINOMYCIN;STREPTOMYCIN'], ['2296669', 'mph(E)', '100.00', '100.00', 'ncbi', 'NG_064660.1', "Mph(E) family macrolide 2'-phosphotransferase", 'MACROLIDE'], ['2296669', 'msr(E)', '100.00', '100.00', 'ncbi', 'NG_048007.1', 'ABC-F type ribosomal protection protein Msr(E)', 'MACROLIDE'], ['2296669', "aac(6')-Ip", '100.00', '99.66', 'ncbi', 'NG_047307.2', "aminoglycoside 6'-N-acetyltransferase AAC(6')-Ip", 'AMINOGLYCOSIDE'], ['2296669', 'aac(3)-Ia', '100.00', '100.00', 'ncbi', 'NG_047234.1', 'aminoglycoside N-acetyltransferase AAC(3)-Ia', 'GENTAMICIN'], ['2296669', 'blaOXA-72', '100.00', '100.00', 'ncbi', 'NG_049813.1', 'OXA-24 family carbapenem-hydrolyzing class D beta-lactamase OXA-72', 'CARBAPENEM']]})
        #run_DB_push("/Usersclear/adrian/Documents/GitHub/CRAB_Analysis",['22222'],{'2296669_manualy': ['2296669', 'abaumannii_2', '2']},{'2296669_blaADC-30': ['2296669', 'blaADC-30', '100.00', '100.00', 'ncbi', 'NG_048652.1', 'class C extended-spectrum beta-lactamase ADC-30', 'CEPHALOSPORIN'], '2296669_tet(B)': ['2296669', 'tet(B)', '99.50', '100.00', 'ncbi', 'NG_048161.1', 'tetracycline efflux MFS transporter Tet(B)', 'TETRACYCLINE'], '2296669_aph(6)-Id': ['2296669', 'aph(6)-Id', '100.00', '100.00', 'ncbi', 'NG_047464.1', 'aminoglycoside O-phosphotransferase APH(6)-Id', 'STREPTOMYCIN'], "2296669_aph(3'')-Ib": ['2296669', "aph(3'')-Ib", '98.31', '99.88', 'ncbi', 'NG_056002.2', "aminoglycoside O-phosphotransferase APH(3'')-Ib", 'STREPTOMYCIN'], '2296669_blaOXA-66': ['2296669', 'blaOXA-66', '100.00', '100.00', 'ncbi', 'NG_049806.1', 'OXA-51 family carbapenem-hydrolyzing class D beta-lactamase OXA-66', 'CARBAPENEM'], '2296669_sul2': ['2296669', 'sul2', '100.00', '100.00', 'ncbi', 'NG_051852.1', 'sulfonamide-resistant dihydropteroate synthase Sul2', 'SULFONAMIDE'], "2296669_ant(3'')-IIa": ['2296669', "ant(3'')-IIa", '100.00', '98.61', 'ncbi', 'NG_054646.1', "aminoglycoside nucleotidyltransferase ANT(3'')-IIa", 'SPECTINOMYCIN;STREPTOMYCIN'], '2296669_mph(E)': ['2296669', 'mph(E)', '100.00', '100.00', 'ncbi', 'NG_064660.1', "Mph(E) family macrolide 2'-phosphotransferase", 'MACROLIDE'], '2296669_msr(E)': ['2296669', 'msr(E)', '100.00', '100.00', 'ncbi', 'NG_048007.1', 'ABC-F type ribosomal protection protein Msr(E)', 'MACROLIDE'], "2296669_aac(6')-Ip": ['2296669', "aac(6')-Ip", '100.00', '99.66', 'ncbi', 'NG_047307.2', "aminoglycoside 6'-N-acetyltransferase AAC(6')-Ip", 'AMINOGLYCOSIDE'], '2296669_aac(3)-Ia': ['2296669', 'aac(3)-Ia', '100.00', '100.00', 'ncbi', 'NG_047234.1', 'aminoglycoside N-acetyltransferase AAC(3)-Ia', 'GENTAMICIN'], '2296669_blaOXA-72': ['2296669', 'blaOXA-72', '100.00', '100.00', 'ncbi', 'NG_049813.1', 'OXA-24 family carbapenem-hydrolyzing class D beta-lactamase OXA-72', 'CARBAPENEM']})

        #3.5 workflow to pull contigs into assembled genome
        #then do snp stuff 
        #and phylogenetic things
        run_WF_3_5(path_to_reads,sample_HSN, path_to_shuffled_reads,run_date,path_to_referance_genome, path_to_snp_output )

        #WF_4 report generation
        #Phylogentics Tree of all samples on run
        #SNP heat map of all samples
        #bring together all information



def CRAB_pipeline(path_to_reads,sample_sheet_p):

    #will be turned to class then read in as self vars

    assembly_output="/home/ks_khel/CRAB_OUT/"
    assembly_output="/Users/adrian/Desktop/CRAB_TESTING/Assembled"
    parent_dir_path="/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[:-1])  #path minus scripts 
    prokka_output="/Users/adrian/Desktop/CRAB_TESTING/Prokka"
    abricate_output = "/Users/adrian/Desktop/CRAB_TESTING/Abricate"
    busco_output = "/Users/adrian/Desktop/CRAB_TESTING/Busco"
    path_to_referance_genome =""
    path_to_shuffled_reads=""
    path_to_snp_output=""
    path_to_tree_output=""
    path_to_pdf_output=""

    #run date will be name of the CSV file
    run_date = sample_sheet_p.split("/")[-1]
    run_date= run_date.split("_")[0]
    
    #organism verfication

    #WF_0
    #Fastq pre proccessing, runs SPADES assembler, RETURNS list of HSN
    #sample_HSN , Assembly_stats = run_assembly(parent_dir_path,path_to_reads,assembly_output,busco_output)
    print("Assembly Done")

    sample_HSN =['2278019', '2278016', '2281037', '2281793']

    #WF_1
    #runs Prokka
    #runs MLST typing, RETURNS MLST TYPE in DICT {"HSH":[species,type, something, ...]} 
                                                #{'2296669_manualy': ['2296669_manualy', 'abaumannii_2', '2']}
    #mlst = run_annotate(assembly_output,prokka_output,sample_HSN)
    print("Annotation Done")
    

    #WF_2
    #Runs Abricate, converts the output to something to be pushed to DB
    
    #found_genes = find_AMR_genes(sample_HSN,assembly_output,abricate_output)
    print("found AMR genes")

    #found_genes DICT {HSN:[GENE,%COV,%IDENT,DB_Used,Accession_Seq,Gene_Product,Resistance]}

    #WF_3 DB push
    #demographical push
    #gene and anti-micorable data
    #MLST typing 
    #run_DB_push(parent_dir_path,sample_HSN,mlst,found_genes) #this one!!!!

    #3.5 workflow to pull contigs into assembled genome
    #then do snp stuff 
    #and phylogenetic things
    #run_WF_3_5(path_to_reads,sample_HSN, path_to_shuffled_reads,run_date,path_to_referance_genome, path_to_snp_output,path_to_tree_output, assembly_output )

    #WF_4 report generation
    #Phylogentics Tree of all samples on run
    #SNP heat map of all samples
    #bring together all information
   # run_create_PDF(sample_HSN,run_date, path_to_pdf_output ,parent_dir_path,found_genes, mlst,path_to_snp_output )

if __name__ == "__main__":

    CRAB_pipeline("/Users/adrian/Desktop/CRAB_DATA/062422","/Users/adrian/Desktop/CRAB_DATA/062422_samplesheet.csv")