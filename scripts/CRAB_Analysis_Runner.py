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

    def __init__(self, cache_path) :
        self.cache_path = cache_path
        #self.path_to_reads = path_to_reads
        #self.sample_sheet_p = sample_sheet_p
        #self.run_data = sample_sheet_p.split("/")[-1][:-4]

        demo_cahce= reader.read_json(cache_path+"/data/pipeline_variables.json")

        for item in [*demo_cahce] :
            setattr(self,item, demo_cahce[item])

    def run_pipeline(self,path_to_reads,run_date):
        
        #WF_0
        #Fastq pre proccessing, runs SPADES assembler, RETURNS list of HSN
        #sample_HSN , Assembly_stats = run_assembly(self.cache_path,path_to_reads,self.assembly_output,self.busco_output,run_date)
        sample_HSN=['2421060', '2405133', '2432808', '2432807', '2431275', '2414529', '2445823', '2439154']
        print(sample_HSN)
        Assembly_stats={'2421060': 'C:98.4%[S:98.4%,D:0.0%],F:1.6%,M:0.0%,n:124', '2405133': 'C:98.4%[S:98.4%,D:0.0%],F:1.6%,M:0.0%,n:124', '2432808': 'C:98.4%[S:98.4%,D:0.0%],F:1.6%,M:0.0%,n:124', '2432807': 'C:98.4%[S:98.4%,D:0.0%],F:1.6%,M:0.0%,n:124', '2431275': 'C:98.4%[S:97.6%,D:0.8%],F:1.6%,M:0.0%,n:124', '2414529': 'C:98.4%[S:98.4%,D:0.0%],F:1.6%,M:0.0%,n:124', '2445823': 'C:98.4%[S:98.4%,D:0.0%],F:1.6%,M:0.0%,n:124', '2439154': 'C:98.4%[S:98.4%,D:0.0%],F:1.6%,M:0.0%,n:124'}
        print(Assembly_stats)
        
        print("Assembly Done")
        mlst={'2421060': ['2421060', 'abaumannii_2', '2'], '2405133': ['2405133', 'abaumannii_2', '2'], '2432808': ['2432808', 'abaumannii_2', '2'], '2432807': ['2432807', 'abaumannii_2', '2'], '2431275': ['2431275', 'abaumannii_2', '499'], '2414529': ['2414529', 'abaumannii_2', '2'], '2445823': ['2445823', 'abaumannii_2', '1'], '2439154': ['2439154', 'abaumannii_2', '499']}
        #WF_1
        #runs Prokka
        #runs MLST typing, RETURNS MLST TYPE in DICT {"HSH":[species,type, something, ...]} 
                                                    #{'2296669_manualy': ['2296669_manualy', 'abaumannii_2', '2']}
        self.assembly_output+="/"+run_date  
        self.prokka_output+="/"+run_date      
        #mlst = run_annotate(self.assembly_output,self.prokka_output,sample_HSN)
        print("Annotation Done")
        print(mlst)

        #WF_2
        #Runs Abricate, converts the output to something to be pushed to DB
        self.abricate_output+="/"+run_date 
        #found_genes = find_AMR_genes(sample_HSN,self.assembly_output,self.abricate_output)
        found_genes={'2421060_blaADC-30': ['2421060', 'blaADC-30', '100.00', '100.00', 'ncbi', 'NG_048652.1', 'class C extended-spectrum beta-lactamase ADC-30', 'CEPHALOSPORIN'], "2421060_aph(3'')-Ib": ['2421060', "aph(3'')-Ib", '98.31', '99.88', 'ncbi', 'NG_056002.2', "aminoglycoside O-phosphotransferase APH(3'')-Ib", 'STREPTOMYCIN'], '2421060_aph(6)-Id': ['2421060', 'aph(6)-Id', '100.00', '100.00', 'ncbi', 'NG_047464.1', 'aminoglycoside O-phosphotransferase APH(6)-Id', 'STREPTOMYCIN'], '2421060_tet(B)': ['2421060', 'tet(B)', '99.50', '100.00', 'ncbi', 'NG_048161.1', 'tetracycline efflux MFS transporter Tet(B)', 'TETRACYCLINE'], '2421060_blaOXA-66': ['2421060', 'blaOXA-66', '100.00', '100.00', 'ncbi', 'NG_049806.1', 'OXA-51 family carbapenem-hydrolyzing class D beta-lactamase OXA-66', 'CARBAPENEM'], "2421060_ant(3'')-IIa": ['2421060', "ant(3'')-IIa", '100.00', '98.61', 'ncbi', 'NG_054646.1', "aminoglycoside nucleotidyltransferase ANT(3'')-IIa", 'SPECTINOMYCIN;STREPTOMYCIN'], '2421060_dfrA17': ['2421060', 'dfrA17', '100.00', '99.79', 'ncbi', 'NG_047710.1', 'trimethoprim-resistant dihydrofolate reductase DfrA17', 'TRIMETHOPRIM'], '2421060_aadA5': ['2421060', 'aadA5', '100.00', '100.00', 'ncbi', 'NG_047357.1', "ANT(3'')-Ia family aminoglycoside nucleotidyltransferase AadA5", 'STREPTOMYCIN'], '2421060_sul1': ['2421060', 'sul1', '100.00', '100.00', 'ncbi', 'NG_048082.1', 'sulfonamide-resistant dihydropteroate synthase Sul1', 'SULFONAMIDE'], '2421060_aac(3)-Ia': ['2421060', 'aac(3)-Ia', '100.00', '100.00', 'ncbi', 'NG_047234.1', 'aminoglycoside N-acetyltransferase AAC(3)-Ia', 'GENTAMICIN'], "2421060_aac(6')-Ip": ['2421060', "aac(6')-Ip", '100.00', '99.66', 'ncbi', 'NG_047307.2', "aminoglycoside 6'-N-acetyltransferase AAC(6')-Ip", 'AMINOGLYCOSIDE'], '2421060_blaOXA-72': ['2421060', 'blaOXA-72', '100.00', '100.00', 'ncbi', 'NG_049813.1', 'OXA-24 family carbapenem-hydrolyzing class D beta-lactamase OXA-72', 'CARBAPENEM'], '2405133_blaADC-30': ['2405133', 'blaADC-30', '100.00', '100.00', 'ncbi', 'NG_048652.1', 'class C extended-spectrum beta-lactamase ADC-30', 'CEPHALOSPORIN'], "2405133_aph(3'')-Ib": ['2405133', "aph(3'')-Ib", '98.31', '99.88', 'ncbi', 'NG_056002.2', "aminoglycoside O-phosphotransferase APH(3'')-Ib", 'STREPTOMYCIN'], '2405133_aph(6)-Id': ['2405133', 'aph(6)-Id', '100.00', '100.00', 'ncbi', 'NG_047464.1', 'aminoglycoside O-phosphotransferase APH(6)-Id', 'STREPTOMYCIN'], '2405133_tet(B)': ['2405133', 'tet(B)', '99.50', '100.00', 'ncbi', 'NG_048161.1', 'tetracycline efflux MFS transporter Tet(B)', 'TETRACYCLINE'], '2405133_blaOXA-66': ['2405133', 'blaOXA-66', '100.00', '100.00', 'ncbi', 'NG_049806.1', 'OXA-51 family carbapenem-hydrolyzing class D beta-lactamase OXA-66', 'CARBAPENEM'], "2405133_ant(3'')-IIa": ['2405133', "ant(3'')-IIa", '100.00', '98.61', 'ncbi', 'NG_054646.1', "aminoglycoside nucleotidyltransferase ANT(3'')-IIa", 'SPECTINOMYCIN;STREPTOMYCIN'], '2405133_aac(3)-Ia': ['2405133', 'aac(3)-Ia', '100.00', '100.00', 'ncbi', 'NG_047234.1', 'aminoglycoside N-acetyltransferase AAC(3)-Ia', 'GENTAMICIN'], '2405133_sul2': ['2405133', 'sul2', '100.00', '100.00', 'ncbi', 'NG_051852.1', 'sulfonamide-resistant dihydropteroate synthase Sul2', 'SULFONAMIDE'], "2405133_aac(6')-Ip": ['2405133', "aac(6')-Ip", '100.00', '99.66', 'ncbi', 'NG_047307.2', "aminoglycoside 6'-N-acetyltransferase AAC(6')-Ip", 'AMINOGLYCOSIDE'], '2405133_blaOXA-72': ['2405133', 'blaOXA-72', '100.00', '100.00', 'ncbi', 'NG_049813.1', 'OXA-24 family carbapenem-hydrolyzing class D beta-lactamase OXA-72', 'CARBAPENEM'], '2432808_sul2': ['2432808', 'sul2', '100.00', '100.00', 'ncbi', 'NG_051852.1', 'sulfonamide-resistant dihydropteroate synthase Sul2', 'SULFONAMIDE'], "2432808_aac(6')-Ip": ['2432808', "aac(6')-Ip", '100.00', '99.66', 'ncbi', 'NG_047307.2', "aminoglycoside 6'-N-acetyltransferase AAC(6')-Ip", 'AMINOGLYCOSIDE'], '2432808_blaADC-30': ['2432808', 'blaADC-30', '100.00', '100.00', 'ncbi', 'NG_048652.1', 'class C extended-spectrum beta-lactamase ADC-30', 'CEPHALOSPORIN'], '2432808_blaOXA-72': ['2432808', 'blaOXA-72', '100.00', '100.00', 'ncbi', 'NG_049813.1', 'OXA-24 family carbapenem-hydrolyzing class D beta-lactamase OXA-72', 'CARBAPENEM'], "2432808_ant(3'')-IIa": ['2432808', "ant(3'')-IIa", '100.00', '98.61', 'ncbi', 'NG_054646.1', "aminoglycoside nucleotidyltransferase ANT(3'')-IIa", 'SPECTINOMYCIN;STREPTOMYCIN'], "2432808_aph(3'')-Ib": ['2432808', "aph(3'')-Ib", '98.31', '99.88', 'ncbi', 'NG_056002.2', "aminoglycoside O-phosphotransferase APH(3'')-Ib", 'STREPTOMYCIN'], '2432808_aph(6)-Id': ['2432808', 'aph(6)-Id', '100.00', '100.00', 'ncbi', 'NG_047464.1', 'aminoglycoside O-phosphotransferase APH(6)-Id', 'STREPTOMYCIN'], '2432808_tet(B)': ['2432808', 'tet(B)', '99.50', '100.00', 'ncbi', 'NG_048161.1', 'tetracycline efflux MFS transporter Tet(B)', 'TETRACYCLINE'], '2432808_mph(E)': ['2432808', 'mph(E)', '100.00', '100.00', 'ncbi', 'NG_064660.1', "Mph(E) family macrolide 2'-phosphotransferase", 'MACROLIDE'], '2432808_msr(E)': ['2432808', 'msr(E)', '100.00', '100.00', 'ncbi', 'NG_048007.1', 'ABC-F type ribosomal protection protein Msr(E)', 'MACROLIDE'], '2432808_armA': ['2432808', 'armA', '100.00', '100.00', 'ncbi', 'NG_047476.1', 'ArmA family 16S rRNA (guanine(1405)-N(7))-methyltransferase', 'GENTAMICIN'], '2432808_sul1': ['2432808', 'sul1', '100.00', '100.00', 'ncbi', 'NG_048082.1', 'sulfonamide-resistant dihydropteroate synthase Sul1', 'SULFONAMIDE'], '2432808_aadA5': ['2432808', 'aadA5', '100.00', '100.00', 'ncbi', 'NG_047357.1', "ANT(3'')-Ia family aminoglycoside nucleotidyltransferase AadA5", 'STREPTOMYCIN'], '2432808_dfrA17': ['2432808', 'dfrA17', '100.00', '99.79', 'ncbi', 'NG_047710.1', 'trimethoprim-resistant dihydrofolate reductase DfrA17', 'TRIMETHOPRIM'], '2432808_blaOXA-66': ['2432808', 'blaOXA-66', '100.00', '100.00', 'ncbi', 'NG_049806.1', 'OXA-51 family carbapenem-hydrolyzing class D beta-lactamase OXA-66', 'CARBAPENEM'], '2432808_aac(3)-Ia': ['2432808', 'aac(3)-Ia', '100.00', '100.00', 'ncbi', 'NG_047234.1', 'aminoglycoside N-acetyltransferase AAC(3)-Ia', 'GENTAMICIN'], '2432807_blaADC-30': ['2432807', 'blaADC-30', '100.00', '100.00', 'ncbi', 'NG_048652.1', 'class C extended-spectrum beta-lactamase ADC-30', 'CEPHALOSPORIN'], "2432807_aph(3'')-Ib": ['2432807', "aph(3'')-Ib", '98.31', '99.88', 'ncbi', 'NG_056002.2', "aminoglycoside O-phosphotransferase APH(3'')-Ib", 'STREPTOMYCIN'], '2432807_aph(6)-Id': ['2432807', 'aph(6)-Id', '100.00', '100.00', 'ncbi', 'NG_047464.1', 'aminoglycoside O-phosphotransferase APH(6)-Id', 'STREPTOMYCIN'], '2432807_tet(B)': ['2432807', 'tet(B)', '99.50', '100.00', 'ncbi', 'NG_048161.1', 'tetracycline efflux MFS transporter Tet(B)', 'TETRACYCLINE'], '2432807_blaOXA-66': ['2432807', 'blaOXA-66', '100.00', '100.00', 'ncbi', 'NG_049806.1', 'OXA-51 family carbapenem-hydrolyzing class D beta-lactamase OXA-66', 'CARBAPENEM'], "2432807_ant(3'')-IIa": ['2432807', "ant(3'')-IIa", '100.00', '98.61', 'ncbi', 'NG_054646.1', "aminoglycoside nucleotidyltransferase ANT(3'')-IIa", 'SPECTINOMYCIN;STREPTOMYCIN'], '2432807_msr(E)': ['2432807', 'msr(E)', '100.00', '100.00', 'ncbi', 'NG_048007.1', 'ABC-F type ribosomal protection protein Msr(E)', 'MACROLIDE'], '2432807_mph(E)': ['2432807', 'mph(E)', '100.00', '100.00', 'ncbi', 'NG_064660.1', "Mph(E) family macrolide 2'-phosphotransferase", 'MACROLIDE'], '2432807_aac(3)-Ia': ['2432807', 'aac(3)-Ia', '100.00', '100.00', 'ncbi', 'NG_047234.1', 'aminoglycoside N-acetyltransferase AAC(3)-Ia', 'GENTAMICIN'], '2432807_sul2': ['2432807', 'sul2', '100.00', '100.00', 'ncbi', 'NG_051852.1', 'sulfonamide-resistant dihydropteroate synthase Sul2', 'SULFONAMIDE'], "2432807_aac(6')-Ip": ['2432807', "aac(6')-Ip", '100.00', '99.66', 'ncbi', 'NG_047307.2', "aminoglycoside 6'-N-acetyltransferase AAC(6')-Ip", 'AMINOGLYCOSIDE'], '2432807_blaOXA-72': ['2432807', 'blaOXA-72', '100.00', '100.00', 'ncbi', 'NG_049813.1', 'OXA-24 family carbapenem-hydrolyzing class D beta-lactamase OXA-72', 'CARBAPENEM'], '2431275_blaOXA-24': ['2431275', 'blaOXA-24', '100.00', '100.00', 'ncbi', 'NG_049534.1', 'carbapenem-hydrolyzing class D beta-lactamase OXA-24', 'CARBAPENEM'], '2431275_blaOXA-95': ['2431275', 'blaOXA-95', '100.00', '100.00', 'ncbi', 'NG_049836.1', 'OXA-51 family carbapenem-hydrolyzing class D beta-lactamase OXA-95', 'CARBAPENEM'], '2431275_blaADC-222': ['2431275', 'blaADC-222', '100.00', '100.00', 'ncbi', 'NG_067193.1', 'class C beta-lactamase ADC-222', 'CEPHALOSPORIN'], "2431275_ant(3'')-IIa": ['2431275', "ant(3'')-IIa", '100.00', '99.49', 'ncbi', 'NG_054648.1', "aminoglycoside nucleotidyltransferase ANT(3'')-IIa", 'SPECTINOMYCIN;STREPTOMYCIN'], "2414529_aph(3'')-Ib": ['2414529', "aph(3'')-Ib", '98.31', '99.88', 'ncbi', 'NG_056002.2', "aminoglycoside O-phosphotransferase APH(3'')-Ib", 'STREPTOMYCIN'], '2414529_aph(6)-Id': ['2414529', 'aph(6)-Id', '100.00', '100.00', 'ncbi', 'NG_047464.1', 'aminoglycoside O-phosphotransferase APH(6)-Id', 'STREPTOMYCIN'], '2414529_tet(B)': ['2414529', 'tet(B)', '99.50', '100.00', 'ncbi', 'NG_048161.1', 'tetracycline efflux MFS transporter Tet(B)', 'TETRACYCLINE'], '2414529_blaADC-30': ['2414529', 'blaADC-30', '100.00', '100.00', 'ncbi', 'NG_048652.1', 'class C extended-spectrum beta-lactamase ADC-30', 'CEPHALOSPORIN'], '2414529_blaOXA-66': ['2414529', 'blaOXA-66', '100.00', '100.00', 'ncbi', 'NG_049806.1', 'OXA-51 family carbapenem-hydrolyzing class D beta-lactamase OXA-66', 'CARBAPENEM'], "2414529_ant(3'')-IIa": ['2414529', "ant(3'')-IIa", '100.00', '98.61', 'ncbi', 'NG_054646.1', "aminoglycoside nucleotidyltransferase ANT(3'')-IIa", 'SPECTINOMYCIN;STREPTOMYCIN'], '2414529_dfrA17': ['2414529', 'dfrA17', '100.00', '99.79', 'ncbi', 'NG_047710.1', 'trimethoprim-resistant dihydrofolate reductase DfrA17', 'TRIMETHOPRIM'], '2414529_aadA5': ['2414529', 'aadA5', '100.00', '100.00', 'ncbi', 'NG_047357.1', "ANT(3'')-Ia family aminoglycoside nucleotidyltransferase AadA5", 'STREPTOMYCIN'], '2414529_sul1': ['2414529', 'sul1', '100.00', '100.00', 'ncbi', 'NG_048082.1', 'sulfonamide-resistant dihydropteroate synthase Sul1', 'SULFONAMIDE'], '2414529_armA': ['2414529', 'armA', '100.00', '100.00', 'ncbi', 'NG_047476.1', 'ArmA family 16S rR (guanine(1405)-N(7))-methyltransferase', 'GENTAMICIN'], '2414529_msr(E)': ['2414529', 'msr(E)', '100.00', '100.00', 'ncbi', 'NG_048007.1', 'ABC-F type ribosomal protection protein Msr(E)', 'MACROLIDE'], '2414529_mph(E)': ['2414529', 'mph(E)', '100.00', '100.00', 'ncbi', 'NG_064660.1', "Mph(E) family macrolide 2'-phosphotransferase", 'MACROLIDE'], '2414529_blaTEM-12': ['2414529', 'blaTEM-12', '100.00', '99.88', 'ncbi', 'NG_050163.1', 'class A extended-spectrum beta-lactamase TEM-12', 'CEPHALOSPORIN'], "2414529_aph(3')-Ia": ['2414529', "aph(3')-Ia", '100.00', '100.00', 'ncbi', 'NG_047431.1', "aminoglycoside O-phosphotransferase APH(3')-Ia", 'KANAMYCIN'], "2414529_aac(6')-Ip": ['2414529', "aac(6')-Ip", '100.00', '99.66', 'ncbi', 'NG_047307.2', "aminoglycoside 6'-N-acetyltransferase AAC(6')-Ip", 'AMINOGLYCOSIDE'], '2414529_blaOXA-72': ['2414529', 'blaOXA-72', '100.00', '100.00', 'ncbi', 'NG_049813.1', 'OXA-24 family carbapenem-hydrolyzing class D beta-lactamase OXA-72', 'CARBAPENEM'], '2445823_blaADC-73': ['2445823', 'blaADC-73', '100.00', '100.00', 'ncbi', 'NG_048678.1', 'class C extended-spectrum beta-lactamase ADC-73', 'CEPHALOSPORIN'], '2445823_blaOXA-69': ['2445823', 'blaOXA-69', '100.00', '100.00', 'ncbi', 'NG_049809.1', 'OXA-51 family carbapenem-hydrolyzing class D beta-lactamase OXA-69', 'CARBAPENEM'], '2445823_blaOXA-23': ['2445823', 'blaOXA-23', '100.00', '100.00', 'ncbi', 'NG_049525.1', 'carbapenem-hydrolyzing class D beta-lactamase OXA-23', 'CARBAPENEM'], "2445823_ant(3'')-IIa": ['2445823', "ant(3'')-IIa", '100.00', '100.00', 'ncbi', 'NG_054646.1', "aminoglycoside nucleotidyltransferase ANT(3'')-IIa", 'SPECTINOMYCIN;STREPTOMYCIN'], "2439154_ant(2'')-Ia": ['2439154', "ant(2'')-Ia", '100.00', '100.00', 'ncbi', 'NG_047387.1', "aminoglycoside nucleotidyltransferase ANT(2'')-Ia", 'GENTAMICIN;KANAMYCIN;TOBRAMYCIN'], '2439154_catB3': ['2439154', 'catB3', '100.00', '100.00', 'ncbi', 'NG_047604.1', 'type B-3 chloramphenicol O-acetyltransferase CatB3', 'CHLORAMPHENICOL'], '2439154_sul1': ['2439154', 'sul1', '100.00', '100.00', 'ncbi', 'NG_048081.1', 'sulfonamide-resistant dihydropteroate synthase Sul1', 'SULFONAMIDE'], '2439154_mph(E)': ['2439154', 'mph(E)', '100.00', '100.00', 'ncbi', 'NG_064660.1', "Mph(E) family macrolide 2'-phosphotransferase", 'MACROLIDE'], '2439154_msr(E)': ['2439154', 'msr(E)', '100.00', '100.00', 'ncbi', 'NG_048007.1', 'ABC-F type ribosomal protection protein Msr(E)', 'MACROLIDE'], '2439154_blaOXA-23': ['2439154', 'blaOXA-23', '100.00', '100.00', 'ncbi', 'NG_049525.1', 'carbapenem-hydrolyzing class D beta-lactamase OXA-23', 'CARBAPENEM'], "2439154_ant(3'')-IIa": ['2439154', "ant(3'')-IIa", '100.00', '98.61', 'ncbi', 'NG_054646.1', "aminoglycoside nucleotidyltransferase ANT(3'')-IIa", 'SPECTINOMYCIN;STREPTOMYCIN'], '2439154_blaADC-222': ['2439154', 'blaADC-222', '100.00', '100.00', 'ncbi', 'NG_067193.1', 'class C beta-lactamase ADC-222', 'CEPHALOSPORIN'], '2439154_blaOXA-95': ['2439154', 'blaOXA-95', '100.00', '100.00', 'ncbi', 'NG_049836.1', 'OXA-51 family carbapenem-hydrolyzing class D beta-lactamase OXA-95', 'CARBAPENEM'], "2439154_aph(3'')-Ib": ['2439154', "aph(3'')-Ib", '98.31', '99.88', 'ncbi', 'NG_056002.2', "aminoglycoside O-phosphotransferase APH(3'')-Ib", 'STREPTOMYCIN'], '2439154_aph(6)-Id': ['2439154', 'aph(6)-Id', '100.00', '100.00', 'ncbi', 'NG_047464.1', 'aminoglycoside O-phosphotransferase APH(6)-Id', 'STREPTOMYCIN'], '2439154_tet(B)': ['2439154', 'tet(B)', '99.50', '100.00', 'ncbi', 'NG_048161.1', 'tetracycline efflux MFS transporter Tet(B)', 'TETRACYCLINE']}
        print(found_genes)
        print("found AMR genes")
   
                #found_genes DICT {HSN:[GENE,%COV,%IDENT,DB_Used,Accession_Seq,Gene_Product,Resistance]}

        #WF_3 DB push
        #demographical push
        #gene and anti-micorable data
        #MLST typing 
        #run_DB_push(self.cache_path,sample_HSN,mlst,found_genes,Assembly_stats,run_date,self.csv_path) 
        print("Push data to DB")
    
        #3.5 workflow to pull contigs into assembled genome
        #then do snp stuff 
        #and phylogenetic things
        run_WF_3_5(path_to_reads,sample_HSN, self.path_to_shuffled_reads,run_date,self.path_to_referance_genome, self.path_to_snp_output )
        print("Sequences Aligned")
        
        #WF_4 report generation
        #Phylogentics Tree of all samples on run
        #SNP heat map of all samples
        #bring together all information

        run_create_PDF(sample_HSN,run_date, self.path_to_pdf_output ,self.cache_path,found_genes, mlst,self.path_to_snp_output )
        print("Report Generated!")




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
    sample_HSN , Assembly_stats = run_assembly(parent_dir_path,path_to_reads,assembly_output,busco_output)
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
    run_DB_push(parent_dir_path,sample_HSN,mlst,found_genes) #this one!!!!

    #3.5 workflow to pull contigs into assembled genome
    #then do snp stuff 
    #and phylogenetic things
    run_WF_3_5(path_to_reads,sample_HSN, path_to_shuffled_reads,run_date,path_to_referance_genome, path_to_snp_output,path_to_tree_output, assembly_output )

    #WF_4 report generation
    #Phylogentics Tree of all samples on run
    #SNP heat map of all samples
    #bring together all information
    run_create_PDF(sample_HSN,run_date, path_to_pdf_output ,parent_dir_path,found_genes, mlst,path_to_snp_output )

if __name__ == "__main__":
    
    dir_path = "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[:-1]) #path minus scripts 
            #TO DO
        #Add assembler stats into WF_
        #also create clean up function to delete all random grabo data
    print(sys.argv)
    input_path = sys.argv[1]
    rundate = sys.argv[2]
    print(input_path)
    print("-----------")
    print(rundate)
    print("-----------")
 
    CRAB_p = CRAB_pipeline_worker(dir_path)
       
    CRAB_p.run_pipeline(input_path,rundate)

   # CRAB_pipeline("/Users/adrian/Desktop/CRAB_DATA/062422","/Users/adrian/Desktop/CRAB_DATA/062422_samplesheet.csv")