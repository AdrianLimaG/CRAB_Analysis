
from venv import create
from fpdf import FPDF
import re
#needed to produce Tree Image
from Bio import Phylo
from matplotlib import pyplot
import pandas as pd
import seaborn as sns

class PDF(FPDF):

    def __init__(self, orientation, unit , format,  header_path, run_date_wgs ) -> None:
        super().__init__(orientation, unit, format)
        self.resource_p= header_path
        self.run_date = run_date_wgs
    def header(self) :
        #insert logo
                                                        #x,y,height/widtt)
        self.image(self.resource_p+"/resources/kdhe_logo.png",10,8,25)
        self.set_font("times","B",15)
        self.cell(0,10,"WGS Run Date : "+self.run_date, ln=1, align='R')
        self.set_font("times","BU",25)
        self.cell(0,10, 'Sequence Analysis Report', border=False,ln=1, align='C')
        self.set_font("times","B",15)
        self.set_text_color(255,0,0)
        self.cell(0,25,"FOR SURVEILLANCE PURPOSES", ln=True)
        self.ln(5)


    def footer(self):
        #set position
        self.set_y(-15)

        #set font
        self.set_font("times","I",10)

        #page number
        self.cell(0,10, f'Page {self.page_no()}/{{nb}}', align='R' )
    
    def create_table(self,table_data, title='', data_size = 10, title_size=12, align_data='L', align_header='L', cell_width='even', x_start='x_default',emphasize_data=[], emphasize_style=None, emphasize_color=(0,0,0)):
        """
        table_data: 
                    list of lists with first element being list of headers
        title: 
                    (Optional) title of table (optional)
        data_size: 
                    the font size of table data
        title_size: 
                    the font size fo the title of the table
        align_data: 
                    align table data
                    L = left align
                    C = center align
                    R = right align
        align_header: 
                    align table data
                    L = left align
                    C = center align
                    R = right align
        cell_width: 
                    even: evenly distribute cell/column width
                    uneven: base cell size on lenght of cell/column items
                    int: int value for width of each cell/column
                    list of ints: list equal to number of columns with the widht of each cell / column
        x_start: 
                    where the left edge of table should start
        emphasize_data:  
                    which data elements are to be emphasized - pass as list 
                    emphasize_style: the font style you want emphaized data to take
                    emphasize_color: emphasize color (if other than black) 
        
        """
        default_style = self.font_style
        if emphasize_style == None:
            emphasize_style = default_style
        # default_font = self.font_family
        # default_size = self.font_size_pt
        # default_style = self.font_style
        # default_color = self.color # This does not work

        # Get Width of Columns
        def get_col_widths():
            col_width = cell_width
            if col_width == 'even':
                col_width = self.epw / len(data[0]) - 1  # distribute content evenly   # epw = effective page width (width of page not including margins)
            elif col_width == 'uneven':
                col_widths = []

                # searching through columns for largest sized cell (not rows but cols)
                for col in range(len(table_data[0])): # for every row
                    longest = 0 
                    for row in range(len(table_data)):
                        cell_value = str(table_data[row][col])
                        value_length = self.get_string_width(cell_value)
                        if value_length > longest:
                            longest = value_length
                    col_widths.append(longest + 4) # add 4 for padding
                col_width = col_widths



                        ### compare columns 

            elif isinstance(cell_width, list):
                col_width = cell_width  # TODO: convert all items in list to int        
            else:
                # TODO: Add try catch
                col_width = int(col_width)
            return col_width

        # Convert dict to lol
        # Why? because i built it with lol first and added dict func after
        # Is there performance differences?
        if isinstance(table_data, dict):
            header = [key for key in table_data]
            data = []
            for key in table_data:
                value = table_data[key]
                data.append(value)
            # need to zip so data is in correct format (first, second, third --> not first, first, first)
            data = [list(a) for a in zip(*data)]

        else:
            header = table_data[0]
            data = table_data[1:]

        line_height = self.font_size * 2.5

        col_width = get_col_widths()
        self.set_font(size=title_size)

        # Get starting position of x
        # Determin width of table to get x starting point for centred table
        if x_start == 'C':
            table_width = 0
            if isinstance(col_width, list):
                for width in col_width:
                    table_width += width
            else: # need to multiply cell width by number of cells to get table width 
                table_width = col_width * len(table_data[0])
            # Get x start by subtracting table width from self width and divide by 2 (margins)
            margin_width = self.w - table_width
            # TODO: Check if table_width is larger than self width

            center_table = margin_width / 2 # only want width of left margin not both
            x_start = center_table
            self.set_x(x_start)
        elif isinstance(x_start, int):
            self.set_x(x_start)
        elif x_start == 'x_default':
            x_start = self.set_x(self.l_margin)


        # TABLE CREATION #

        # add title
        if title != '':
            self.multi_cell(0, line_height, title, border=0, align='j', ln=3, max_line_height=self.font_size)
            self.ln(line_height) # move cursor back to the left margin

        self.set_font(size=data_size)
        # add header
        y1 = self.get_y()
        if x_start:
            x_left = x_start
        else:
            x_left = self.get_x()
        x_right = self.epw + x_left
        if  not isinstance(col_width, list):
            if x_start:
                self.set_x(x_start)
            for datum in header:
                self.multi_cell(col_width, line_height, datum, border=0, align=align_header, ln=3, max_line_height=self.font_size)
                x_right = self.get_x()
            self.ln(line_height) # move cursor back to the left margin
            y2 = self.get_y()
            self.line(x_left,y1,x_right,y1)
            self.line(x_left,y2,x_right,y2)

            for row in data:
                if x_start: # not sure if I need this
                    self.set_x(x_start)
                for datum in row:
                    if datum in emphasize_data:
                        self.set_text_color(*emphasize_color)
                        self.set_font(style=emphasize_style)
                        self.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size)
                        self.set_text_color(0,0,0)
                        self.set_font(style=default_style)
                    else:
                        self.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named self
                self.ln(line_height) # move cursor back to the left margin
        
        else:
            if x_start:
                self.set_x(x_start)
            for i in range(len(header)):
                datum = header[i]
                self.multi_cell(col_width[i], line_height, datum, border=0, align=align_header, ln=3, max_line_height=self.font_size)
                x_right = self.get_x()
            self.ln(line_height) # move cursor back to the left margin
            y2 = self.get_y()
            self.line(x_left,y1,x_right,y1)
            self.line(x_left,y2,x_right,y2)


            for i in range(len(data)):
                if x_start:
                    self.set_x(x_start)
                row = data[i]
                for i in range(len(row)):
                    datum = row[i]
                    if not isinstance(datum, str):
                        datum = str(datum)
                    adjusted_col_width = col_width[i]
                    if datum in emphasize_data:
                        self.set_text_color(*emphasize_color)
                        self.set_font(style=emphasize_style)
                        self.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size)
                        self.set_text_color(0,0,0)
                        self.set_font(style=default_style)
                    else:
                        self.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named self
                self.ln(line_height) # move cursor back to the left margin
        y3 = self.get_y()
        self.line(x_left,y3,x_right,y3)



def run_create_PDF(samples,run_date, output_pdf_dir ,resource_path,found_genes, mlst_dict,MSA_dir_path ):

    pdf = PDF("P","mm","Letter" ,resource_path,run_date)
    pdf.set_title("Acinetobacter baumannii WGS Sequence Analysis Report "+run_date)
    pdf.set_author("AdrianLimaG/CRAB_Analysis Pipeline Developed for KDHE")
    pdf.alias_nb_pages()

    #pdf.resource_p = resource_path
    pdf.add_page()
    #pdf.header(resource_path)

    pdf.set_auto_page_break(auto=True, margin=15)

    #set fond for text
    pdf.set_font('times','',13)
    #adding texz

    #write intro blurg
    pdf.multi_cell(0,4,str(len([*found_genes]))+" isolates of Acinetobacter baumannii were submitted from the Kansas Department of Health and Environment for whole genome sequencing and relatedness assessment, including using multilocus sequence typing (MLST) and single nucleotide polymorphism (SNP) analysis. Results met quality control parameters set by MDH, which include adequate sequencing coverage and core genome percentages. These data suggest there are some differences between the isolates that are not shown using SNP analysis alone. For further interpretation of the laboratory results, we recommend further incorporation of any available clinical and epidemiologic data. The figures below outline the results.",ln=True)
    pdf.ln(8)


    #Notable Resistance Mechanism Section
    pdf.set_font("times","B",14)
    pdf.cell(0,4,"Notable Resistance Mechanisms", ln=True)
    pdf.ln(3)
    pdf.set_font("times","",12)
    pdf.multi_cell(0,4,"The table below shows B-lactamase genes (bla) identified using the NCBI database. Additional antimicrobial resistance genes that were identified are shown later in the report.", ln=True)
    #Resistance Table
    pdf.ln(5)
    #needed to be a list of list
    bla_gene_table_data, other_genes_table_date = format_table_data(found_genes,mlst_dict,samples)

    pdf.create_table(bla_gene_table_data,'',8,0,"C","C",[20,45,35,30,60],"C") 
    pdf.ln(15)
    
    #SNP_Heat_MAP Section
    pdf.set_font("times","B",14)
    pdf.cell(0,4,"SNP Heat Map", ln=True)
    pdf.ln(3)
    pdf.set_font("times","",12)
    pdf.multi_cell(0,4,"The number of single nucleotide polymorphisms (SNPs) between each sample is shown on the heat map. Referance genome Acinetobacter baumannii (g-proteobacteria) GCA_008632635.1 was used as the reference genome for analysis. Since SNPs are determined based on alignment with the reference genome, if a gene(s) is absent from the reference, there will be no SNP identified. Therefore, there is no set number of SNP differences between isolates that classifies an outbreak. It is important that SNP analysis data and epidemiological information be considered together to understand the entire picture.",ln=True)
    pdf.ln(5)
   #create heat map image
    snp_image= creat_snp_image(MSA_dir_path)
    #insert heat map
    pdf.image(snp_image,x=0,w=200,h=150)
    pdf.ln(10)

    #Phylogenetic Tree
    pdf.set_font("times","B",14)
    pdf.cell(0,4,"Phylogenetic Tree", ln=True)
    pdf.ln(3)
    pdf.set_font("times","",12)
    pdf.multi_cell(0,4,"The phylogenetic tree was generated using SNP analysis obtained from running the Lyve-SET bioinformatics pipeline. Isolates clustered together are considered genetically related and the degree of horizontal distance between branches demonstrates divergence between isolates.",ln=True)
    pdf.ln(5)

        #inser tree
    path_to_phylo_image = create_phlyo_image(MSA_dir_path)
    pdf.image(path_to_phylo_image,x=0,w=200,h=150)
    pdf.ln(10)

    #Additional Resistance Genes
    pdf.set_font("times","B",14)
    pdf.cell(0,4,"Additional Resistance Genes", ln=True)
    pdf.ln(3)
    pdf.set_font("times","",12)
    pdf.multi_cell(0,4,"The table below shows additional resistance genes identified in each isolate using the NCBI database. Identification of resistance genes for these isolates has not been compared with phenotypic susceptibility testing; therefore, correlation has not been determined",ln=1)
    pdf.ln(5)
    pdf.create_table(other_genes_table_date,'',8,0,"C","C","even","C") 
    pdf.ln(15)

    #Methods
    pdf.set_font("times","B",14)
    pdf.cell(0,4,"Methods", ln=True)
    pdf.ln(3)
    pdf.set_font("times","",12)
    #update with what you used to visualize the tree with
    pdf.multi_cell(0,4,"Sequencing data was created using the Illumina MiSeq platform. Sample genomes were preprossed using OpenGene/fastp-0.23.2 and assembled DE NOVO using ablab/SPAdes-3.15. WenchaoLin/Busco-5.4.3 was then used to assess genome assembly and annotation completeness. Assembled genomes were screened for resistance mechanisms using the publically available NCBI database using tseemann/abricate-1.0.1. The multilocus sequence type (MLST) was determined using tseemann/mlst-2.22.1 against PubMLST database. Whole genome SNP analysis was performed using Lyve-SET 1.1.4f. The phylogenetic tree was generated using Lyve-SET 1.1.4f data and vizualized using SOMETHING.",ln=True)
    pdf.ln(10)

    #Closing Remarks
    pdf.set_font("times","B",14)
    pdf.cell(0,4,"Data Prepared by AdrianLimaG/CRAB_Analysis Pipeline", ln=True)
    pdf.ln(3)
    pdf.set_font("times","",12)
    pdf.multi_cell(0,4,"Kansas Department of Health & Environment Laboratories\n6810 SE Dwight Street\nTopeka, KS  66620",ln=True)
    pdf.ln(5)


    #save out pdf
    pdf.output(output_pdf_dir+'/CRAB_WGS_Analysis_'+run_date+'.pdf')

#function should take in all dicts and format into an array of arrays
#array 1 will be the BLA genes tables data
#array 2 will be Addtional Genes table data
def format_table_gene_data(found_genes_dict):
    temp_dict={}
    other_genes={}
    for key in [*found_genes_dict] :
        #means their is a β-lactamase genes (bla) gene found
        if re.search("bla",key) :
            if found_genes_dict[key][0] not in temp_dict :
                #creating key in new dict, and add resistance as it is constant for BLA genes
                temp_dict[found_genes_dict[key][0]] =[""] #,found_genes_dict[key][7]]
            #GENE,Details,Resistance
            #[1,6,7]
            temp_gene = found_genes_dict[key][1]

            #Adding Gene and variant info to array
            if temp_gene[:-3] != "blaADC":

                temp_gene +=" (variant of "+found_genes_dict[key][6].split(" ")[0]+")"

            temp_dict[found_genes_dict[key][0]][0]+=temp_gene+"\n"

            #adding resistance
            #if temp_dict[found_genes_dict[key][0]][1] != found_genes_dict[key][7]:
             #   temp_dict[found_genes_dict[key][0]][1]+="\n"+found_genes_dict[key][7]

        else:
            #this will bring togethe all other resitance for same hsn

            if found_genes_dict[key][0] not in other_genes :
                other_genes[found_genes_dict[key][0]] = []
            #GENE,Details,Resistance
            #[1,6,7]
            other_genes[found_genes_dict[key][0]].append([found_genes_dict[key][1],found_genes_dict[key][6],found_genes_dict[key][7]])    

    return temp_dict,other_genes

def format_table_data(found_genes_d,mlst,samples_list):
    
    other_genes_table_list =[["HSN","Gene", "Mechanisms","Resistance"]]
    bla_genes_table_list=[["HSN","Species ID","Specimen source","MLST (Pasteur)", "Mechanisms"]]
    bla_gene_d, other_g_d = format_table_gene_data(found_genes_d)

    for sample in samples_list:
         #"HSN","Species ID","Specimen source","MLST","Gene", "Mechanisms"
        bla_genes_table_list.append(
            [sample,mlst[sample][1],"Specimen SOURCE",mlst[sample][2],bla_gene_d[sample][0]]
        )
        #"HSN","Gene", "Mechanisms","Resistance"
        print(other_g_d)
        for g in other_g_d[sample]:

            other_genes_table_list.append(
                [sample,g[0],g[1],g[2]]
            )
    
    return bla_genes_table_list, other_genes_table_list

def create_phlyo_image(path_to_newick_file):
    tree = Phylo.read(path_to_newick_file+"/msa/tree.dnd", "newick")
    fig = pyplot.figure(figsize=(20, 30), dpi=1000)
    axes = fig.add_subplot(1, 1, 1)
    Phylo.draw(tree,do_show=False)
    pyplot.savefig(path_to_newick_file+"/Tree.png",dpi=300, bbox_inches = "tight")

    return path_to_newick_file+"/Tree.png"

#from ete3 import Tree
#t = Tree("/Users/adrian/Desktop/msa_linxbox/tree.dnd")
#  t.render("/Users/adrian/Desktop/ete3_Tree.png",dpi=300)

def load_matrix(fpath, delim) :
    matrix = []
    with open(fpath) as instream:
        header = next(instream).rstrip()
        names = header.split(delim)[1:]
        names = [sample.split("-")[0] for sample in names]
        for row in map(str.rstrip, instream):
            temp_row =row.split(delim)[1:]
            temp_row=[w.replace('-', '1') for w in temp_row]
            temp_row=[int(item)for item in temp_row]
            matrix.append( temp_row)
    
    return pd.DataFrame(matrix, index=names, columns=names)

def creat_snp_image(path_To_snp):
    snp =load_matrix(path_To_snp+"/msa/out.pairwiseMatrix.tsv","\t")
    sns.heatmap(snp, xticklabels=snp.columns,yticklabels=snp.columns, cmap="Reds" ,annot=True, fmt=".0f",cbar=False, linewidths=1)
    pyplot.xticks(rotation=0)
    pyplot.yticks(rotation=0)
    #pyplot.show()
    pyplot.savefig(path_To_snp+'snp_matrix.png',dpi=300, bbox_inches = "tight")

    return path_To_snp+'snp_matrix.png'




if __name__ == "__main__":


    genes={
        '2278019_blaOXA-66': ['2278019', 'blaOXA-66', '100.00', '100.00', 'ncbi', 'NG_049806.1', 'OXA-51 family carbapenem-hydrolyzing class D beta-lactamase OXA-66', 'CARBAPENEM'],'2278019_blaADC-30': ['2278019', 'blaADC-30', '100.00', '100.00', 'ncbi', 'NG_048652.1', 'class C extended-spectrum beta-lactamase ADC-30', 'CEPHALOSPORIN'], '2278019_tet(B)': ['2278019', 'tet(B)', '99.50', '100.00', 'ncbi', 'NG_048161.1', 'tetracycline efflux MFS transporter Tet(B)', 'TETRACYCLINE'], '2278019_aph(6)-Id': ['2278019', 'aph(6)-Id', '100.00', '100.00', 'ncbi', 'NG_047464.1', 'aminoglycoside O-phosphotransferase APH(6)-Id', 'STREPTOMYCIN'],"2278019_aph(3'')-Ib": ['2278019', "aph(3'')-Ib", '98.31', '99.88', 'ncbi', 'NG_056002.2', "aminoglycoside O-phosphotransferase APH(3'')-Ib", 'STREPTOMYCIN'], '2278019_mph(E)': ['2278019', 'mph(E)', '100.00', '100.00', 'ncbi', 'NG_064660.1', "Mph(E) family macrolide 2'-phosphotransferase", 'MACROLIDE'], '2278019_msr(E)': ['2278019', 'msr(E)', '100.00', '100.00', 'ncbi', 'NG_048007.1', 'ABC-F type ribosomal protection protein Msr(E)', 'MACROLIDE'], '2278019_aac(3)-Ia': ['2278019', 'aac(3)-Ia', '100.00', '100.00', 'ncbi', 'NG_047234.1', 'aminoglycoside N-acetyltransferase AAC(3)-Ia', 'GENTAMICIN'], '2278019_sul2': ['2278019', 'sul2', '100.00', '100.00', 'ncbi', 'NG_051852.1', 'sulfonamide-resistant dihydropteroate synthase Sul2', 'SULFONAMIDE'], '2278019_blaOXA-72': ['2278019', 'blaOXA-72', '100.00', '100.00', 'ncbi', 'NG_049813.1', 'OXA-24 family carbapenem-hydrolyzing class D beta-lactamase OXA-72', 'CARBAPENEM'],"2278019_ant(3'')-IIa": ['2278019', "ant(3'')-IIa", '100.00', '98.61', 'ncbi', 'NG_054646.1', "aminoglycoside nucleotidyltransferase ANT(3'')-IIa", 'SPECTINOMYCIN;STREPTOMYCIN'], '2278016_blaADC-30': ['2278016', 'blaADC-30', '100.00', '100.00', 'ncbi', 'NG_048652.1', 'class C extended-spectrum beta-lactamase ADC-30', 'CEPHALOSPORIN'], "2278016_aph(3'')-Ib": ['2278016', "aph(3'')-Ib", '98.31', '99.88', 'ncbi', 'NG_056002.2', "aminoglycoside O-phosphotransferase APH(3'')-Ib", 'STREPTOMYCIN'], '2278016_aph(6)-Id': ['2278016', 'aph(6)-Id', '100.00', '100.00', 'ncbi', 'NG_047464.1', 'aminoglycoside O-phosphotransferase APH(6)-Id', 'STREPTOMYCIN'], '2278016_tet(B)': ['2278016', 'tet(B)', '99.50', '100.00', 'ncbi', 'NG_048161.1', 'tetracycline efflux MFS transporter Tet(B)', 'TETRACYCLINE'], '2278016_blaOXA-66': ['2278016', 'blaOXA-66', '100.00', '100.00', 'ncbi', 'NG_049806.1', 'OXA-51 family carbapenem-hydrolyzing class D beta-lactamase OXA-66', 'CARBAPENEM'], '2278016_blaOXA-23': ['2278016', 'blaOXA-23', '100.00', '100.00', 'ncbi', 'NG_049525.1', 'carbapenem-hydrolyzing class D beta-lactamase OXA-23', 'CARBAPENEM'], '2278016_blaOXA-72': ['2278016', 'blaOXA-72', '100.00', '100.00', 'ncbi', 'NG_049813.1', 'OXA-24 family carbapenem-hydrolyzing class D beta-lactamase OXA-72', 'CARBAPENEM'], '2278016_mph(E)': ['2278016', 'mph(E)', '100.00', '100.00', 'ncbi', 'NG_064660.1', "Mph(E) family macrolide 2'-phosphotransferase", 'MACROLIDE'], '2278016_msr(E)': ['2278016', 'msr(E)', '100.00', '100.00', 'ncbi', 'NG_048007.1', 'ABC-F type ribosomal protection protein Msr(E)', 'MACROLIDE'], "2278016_ant(3'')-IIa": ['2278016', "ant(3'')-IIa", '100.00', '98.61', 'ncbi', 'NG_054646.1', "aminoglycoside nucleotidyltransferase ANT(3'')-IIa", 'SPECTINOMYCIN;STREPTOMYCIN'], "2278016_aac(6')-Ip": ['2278016', "aac(6')-Ip", '100.00', '99.66', 'ncbi', 'NG_047307.2', "aminoglycoside 6'-N-acetyltransferase AAC(6')-Ip", 'AMINOGLYCOSIDE'], '2278016_aac(3)-Ia': ['2278016', 'aac(3)-Ia', '100.00', '100.00', 'ncbi', 'NG_047234.1', 'aminoglycoside N-acetyltransferase AAC(3)-Ia', 'GENTAMICIN'], '2281037_blaOXA-66': ['2281037', 'blaOXA-66', '100.00', '100.00', 'ncbi', 'NG_049806.1', 'OXA-51 family carbapenem-hydrolyzing class D beta-lactamase OXA-66', 'CARBAPENEM'], '2281037_blaADC-30': ['2281037', 'blaADC-30', '100.00', '100.00', 'ncbi', 'NG_048652.1', 'class C extended-spectrum beta-lactamase ADC-30', 'CEPHALOSPORIN'], "2281037_ant(3'')-IIa": ['2281037', "ant(3'')-IIa", '100.00', '98.61', 'ncbi', 'NG_054646.1', "aminoglycoside nucleotidyltransferase ANT(3'')-IIa", 'SPECTINOMYCIN;STREPTOMYCIN'], "2281037_aac(6')-Ip": ['2281037', "aac(6')-Ip", '100.00', '99.66', 'ncbi', 'NG_047307.2', "aminoglycoside 6'-N-acetyltransferase AAC(6')-Ip", 'AMINOGLYCOSIDE'], '2281037_aac(3)-Ia': ['2281037', 'aac(3)-Ia', '100.00', '100.00', 'ncbi', 'NG_047234.1', 'aminoglycoside N-acetyltransferase AAC(3)-Ia', 'GENTAMICIN'], '2281037_blaOXA-72': ['2281037', 'blaOXA-72', '100.00', '100.00', 'ncbi', 'NG_049813.1', 'OXA-24 family carbapenem-hydrolyzing class D beta-lactamase OXA-72', 'CARBAPENEM'], '2281037_tet(B)': ['2281037', 'tet(B)', '99.50', '100.00', 'ncbi', 'NG_048161.1', 'tetracycline efflux MFS transporter Tet(B)', 'TETRACYCLINE'], '2281037_aph(6)-Id': ['2281037', 'aph(6)-Id', '100.00', '100.00', 'ncbi', 'NG_047464.1', 'aminoglycoside O-phosphotransferase APH(6)-Id', 'STREPTOMYCIN'], "2281037_aph(3'')-Ib": ['2281037', "aph(3'')-Ib", '98.31', '99.88', 'ncbi', 'NG_056002.2', "aminoglycoside O-phosphotransferase APH(3'')-Ib", 'STREPTOMYCIN'], "2281793_ant(3'')-IIa": ['2281793', "ant(3'')-IIa", '100.00', '98.61', 'ncbi', 'NG_054646.1', "aminoglycoside nucleotidyltransferase ANT(3'')-IIa", 'SPECTINOMYCIN;STREPTOMYCIN'], '2281793_blaADC-30': ['2281793', 'blaADC-30', '100.00', '99.91', 'ncbi', 'NG_048652.1', 'class C extended-spectrum beta-lactamase ADC-30', 'CEPHALOSPORIN'], '2281793_tet(B)': ['2281793', 'tet(B)', '99.50', '100.00', 'ncbi', 'NG_048161.1', 'tetracycline efflux MFS transporter Tet(B)', 'TETRACYCLINE'], '2281793_aph(6)-Id': ['2281793', 'aph(6)-Id', '100.00', '100.00', 'ncbi', 'NG_047464.1', 'aminoglycoside O-phosphotransferase APH(6)-Id', 'STREPTOMYCIN'], "2281793_aph(3'')-Ib": ['2281793', "aph(3'')-Ib", '98.31', '99.88', 'ncbi', 'NG_056002.2', "aminoglycoside O-phosphotransferase APH(3'')-Ib", 'STREPTOMYCIN'], '2281793_blaOXA-66': ['2281793', 'blaOXA-66', '100.00', '100.00', 'ncbi', 'NG_049806.1', 'OXA-51 family carbapenem-hydrolyzing class D beta-lactamase OXA-66', 'CARBAPENEM'], '2281793_dfrA17': ['2281793', 'dfrA17', '100.00', '99.79', 'ncbi', 'NG_047710.1', 'trimethoprim-resistant dihydrofolate reductase DfrA17', 'TRIMETHOPRIM'], '2281793_aadA5': ['2281793', 'aadA5', '100.00', '100.00', 'ncbi', 'NG_047357.1', "ANT(3'')-Ia family aminoglycoside nucleotidyltransferase AadA5", 'STREPTOMYCIN'], '2281793_sul1': ['2281793', 'sul1', '100.00', '100.00', 'ncbi', 'NG_048082.1', 'sulfonamide-resistant dihydropteroate synthase Sul1', 'SULFONAMIDE'], '2281793_armA': ['2281793', 'armA', '100.00', '100.00', 'ncbi', 'NG_047476.1', 'ArmA family 16S rRNA (guanine(1405)-N(7))-methyltransferase', 'GENTAMICIN'], '2281793_msr(E)': ['2281793', 'msr(E)', '100.00', '100.00', 'ncbi', 'NG_048007.1', 'ABC-F type ribosomal protection protein Msr(E)', 'MACROLIDE'], '2281793_mph(E)': ['2281793', 'mph(E)', '100.00', '100.00', 'ncbi', 'NG_064660.1', "Mph(E) family macrolide 2'-phosphotransferase", 'MACROLIDE'], '2281793_aac(3)-Ia': ['2281793', 'aac(3)-Ia', '100.00', '100.00', 'ncbi', 'NG_047234.1', 'aminoglycoside N-acetyltransferase AAC(3)-Ia', 'GENTAMICIN'], '2281793_sul2': ['2281793', 'sul2', '100.00', '100.00', 'ncbi', 'NG_051852.1', 'sulfonamide-resistant dihydropteroate synthase Sul2', 'SULFONAMIDE'], "2281793_aac(6')-Ip": ['2281793', "aac(6')-Ip", '100.00', '99.66', 'ncbi', 'NG_047307.2', "aminoglycoside 6'-N-acetyltransferase AAC(6')-Ip", 'AMINOGLYCOSIDE'], '2281793_blaOXA-72': ['2281793', 'blaOXA-72', '100.00', '100.00', 'ncbi', 'NG_049813.1', 'OXA-24 family carbapenem-hydrolyzing class D beta-lactamase OXA-72', 'CARBAPENEM']
    }
    mls= {'2278019': ['2278019', 'abaumannii_2', '2'], '2278016': ['2278016', 'abaumannii_2', '2'], '2281037': ['2281037', 'abaumannii_2', '2'], '2281793': ['2281793', 'abaumannii_2', '2']}


    run_create_PDF(['2278019', '2278016', '2281037', '2281793'],"062422","/Users/adrian/Desktop",'/Users/adrian/Documents/GitHub/CRAB_Analysis',genes,mls,"/Users/adrian/Desktop")


