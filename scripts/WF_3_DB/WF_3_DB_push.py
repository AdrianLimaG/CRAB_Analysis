from WF_3_DB.WF_3_helper import demographics_import





def run_DB_push(runner_path,sample_hsn,mlst_t,f_genes, assembly_metrics,run_date,csv_paths,CDC=False):
    #assembly metrics contain

            #self.lims_df.apply(lambda row: str(row["hsn"]), axis=1)
        #hsn= item.split("-")[0]
        #[x for x in records.split("\n") if x.strip() != '']
    if not(CDC):
        sample_hsn = [x.split("-")[0] for x in sample_hsn ]

        sample_hsn = list(dict.fromkeys(sample_hsn))

        mlst_t = rname_dict(mlst_t)

        assembly_metrics = rname_dict(assembly_metrics)

        f_genes = rname_dict(f_genes)

    import_demo = demographics_import(runner_path)

    import_demo.get_lims_demographics(sample_hsn,run_date,csv_paths)
    print("lims imported")
    import_demo.format_lims_df()

    import_demo.create_metrics_df(assembly_metrics,CDC) #checks genomes completeness but not depth/coverage

    import_demo.create_mlst_df(mlst_t)

    import_demo.create_genes_df(f_genes)
    #merge_mlst,demogrpahic DF together
    import_demo.merge_dfs()

    import_demo.format_dfs()

    import_demo.database_push(csv_paths,run_date)

    import_demo.database_push_genes()


def rname_dict(working_dic):

    for k in [*working_dic]:
        working_dic[k.split("-")[0]] = []
        working_dic[k.split("-")[0]] = working_dic[k.split("-")[0]].append(working_dic.pop(k))
    
    return working_dic