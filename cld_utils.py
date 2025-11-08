def find_cld_columns(result, result_type):
   
   if result_type == "pg_tk":
      return list(result['A']), list(result['B']), list(result['p-tukey'])
   
   elif result_type == "stm_tk":
      data_table = result._results_table.data
      data_ids =  [data_table[0].index(i) for i in ["group1", "group2", "p-adj"]]
      return [[row[i] for row in data_table[1:]] for i in data_ids]