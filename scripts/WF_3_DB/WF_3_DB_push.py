from WF_3_DB.WF_3_helper import demographics_import


def run_DB_push(runner_path,sample_hsn,mlst_t,f_genes, assembly_metrics):
    #assembly metrics contain

    import_demo = demographics_import(runner_path)

    import_demo.get_lims_demographics(sample_hsn)
    print("lims imported")
    import_demo.format_lims_df()

    import_demo.create_metrics_df(assembly_metrics) #checks genomes completeness but not depth/coverage

    import_demo.create_mlst_df(mlst_t)

    import_demo.create_genes_df(f_genes)
    #merge_mlst,demogrpahic DF together
    import_demo.merge_dfs()

    import_demo.format_dfs()

    import_demo.database_push()

    import_demo.database_push_genes()