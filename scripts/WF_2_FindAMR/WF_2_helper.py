import subprocess
import os

def run_AMR(path_to_contigs,samples,abricate_output):
    if not(os.path.exists(abricate_output)):
            os.mkdir(abricate_output)
    for sample in samples :
        #os.mkdir(abricate_output+"/"+sample)
        subprocess.run(". $CONDA_PREFIX/home/ssh_user/mambaforge/etc/profile.d/conda.sh && conda activate CRAB && abricate "+path_to_contigs+"/"+sample+"/scaffolds.fasta > "+abricate_output+"/"+sample+"_AMRgenes.tsv",shell= True)

def parse_AMR(abricate_output,samples):

    amr_d={}
    for sample in samples:
        #amr_d[sample+"_"+str(g_lines[5])]=[]
        if os.path.exists(abricate_output+"/"+sample+"_AMRgenes.tsv") :
            amr_f = open(abricate_output+"/"+sample+"_AMRgenes.tsv","r")
            amr_content = amr_f.readlines()
            for l in amr_content[1:] :
                g_lines=l.strip().split("\t")
                #GENE,%COVERAGE,%IDENTIT,DB_used,accession, product, resistan
                #print(g_lines)
                amr_d[sample+"_"+str(g_lines[5].strip())] = [sample]+[g_lines[5].strip()]+g_lines[9:]
        else:
            amr_d[sample]=[]

    return amr_d




if __name__ == "__main__":
    #run_AMR("/Users/adrian/Desktop/CRAB_OUT",['2296669_manualy'],"/Users/adrian/Desktop")

    print(parse_AMR("/Users/adrian/Desktop",['2296669']))

    #Desktop/CRAB_OUT/2296669_manualy/scaffolds.fasta 

