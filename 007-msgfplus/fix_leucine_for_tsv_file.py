import os

path = os.getcwd()
output_path = "{0}\\output\\".format(path)
result_out_path = '{0}msgfp_v2\\'.format(output_path)

merged_msgfplus_tsv = '{0}KO_Rpick_Merged.tsv'.format(result_out_path)
merged_msgfplus_i_tsv = '{0}KO_Rpick_Merged_I.tsv'.format(result_out_path)

with open(merged_msgfplus_i_tsv, "w") as file_i:
    with open(merged_msgfplus_tsv) as file:
        for line in file.read().splitlines():
            list_line = line.split('\t')
            list_line[8] = list_line[8].replace('L', 'I') #8 for peptide column index
            file_i.write('\t'.join(list_line) + '\n')