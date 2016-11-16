import os
import pandas as pd
from pandas.core.common import intersection

path = os.getcwd()
input_path = path + "\\input\\"
output_path = path + "\\output\\"

msgfdb_tsv = '{0}KO_RPick_02_23_LTQ_2_24Feb06_Sphinx_06-01-07_msgfdb_fht.txt'.format(input_path)
merged_msgfplus_tsv = '{0}KO_Rpick_Merged.tsv'.format(output_path)
result_file = '{0}matched_pepdtide_results.txt'.format(output_path)


df_msgfdb = pd.read_table(msgfdb_tsv)
df_msgfplus = pd.read_table(merged_msgfplus_tsv)

list_peptide_msgfdb = df_msgfdb['Peptide'].tolist()
list_peptide_msgfplus = df_msgfplus['Peptide'].tolist()

set_msgfdb = set(list_peptide_msgfdb)
set_msgfplus = set(list_peptide_msgfplus)

set_result = intersection(set_msgfdb, set_msgfplus)

with open(result_file, "a") as result:
    result.write(('all peptide count in msgfdb database : {0}\n'.format(list_peptide_msgfdb.__len__())))
    result.write(('all peptide count in msgfplus merged database : {0}\n'.format(list_peptide_msgfplus.__len__())))
    result.write(('unique peptide count in msgfdb database : {0}\n'.format(set_msgfdb.__len__())))
    result.write(('unique peptide count in msgfplus merged database : {0}\n'.format(set_msgfplus.__len__())))
    result.write(('unique peptide matched count between databases : {0}\n'.format(set_result.__len__())))
