import os
import pandas as pd
from pandas.core.common import intersection

path = os.getcwd()
input_path = path + "\\input\\"
output_path = path + "\\output\\"

# msgfdb_tsv = '{0}KO_RPick_02_23_LTQ_2_24Feb06_Sphinx_06-01-07_msgfdb_fht.txt'.format(input_path)
blib_tsv = '{0}Ralstonia_pickettii.blib.tsv'.format(input_path)
merged_msgfplus_tsv = '{0}KO_Rpick_Merged.tsv'.format(output_path)
result_file = '{0}matched_pepdtide_results.txt'.format(output_path)

blib_peptide_file = '{}Ralstonia_pickettii.blib.peptides.txt'.format(output_path)
msgfplus_peptide_file = '{}KO_Rpick_Merged_MsgfPlus.peptides.txt'.format(output_path)
matched_peptide_file = '{}blib_msgfplus_matched_peptides.txt'.format(output_path)

# df_msgfdb = pd.read_table(msgfdb_tsv)
df_blib = pd.read_table(blib_tsv)
df_msgfplus = pd.read_table(merged_msgfplus_tsv)

# list_peptide_msgfdb = df_msgfdb['Peptide'].tolist()
list_peptide_blib = df_blib['peptideSeq'].tolist()
list_peptide_msgfplus = df_msgfplus['Peptide'].tolist()

# set_msgfdb = set(list_peptide_msgfdb)
set_blib = set(list_peptide_blib)
set_msgfplus = set(list_peptide_msgfplus)

set_matched = intersection(set_blib, set_msgfplus)

with open(result_file, "a") as result:
    # result.write(('all peptide count in msgfdb database : {0}\n'.format(list_peptide_msgfdb.__len__())))
    result.write(('all peptide count in blib database : {0}\n'.format(list_peptide_blib.__len__())))
    result.write(('all peptide count in msgfplus merged database : {0}\n'.format(list_peptide_msgfplus.__len__())))
    # result.write(('unique peptide count in msgfdb database : {0}\n'.format(set_msgfdb.__len__())))
    result.write(('unique peptide count in blib database : {0}\n'.format(set_blib.__len__())))
    result.write(('unique peptide count in msgfplus merged database : {0}\n'.format(set_msgfplus.__len__())))
    result.write(('unique peptide matched count between databases : {0}\n'.format(set_matched.__len__())))

with open(blib_peptide_file, "a") as f:
    f.write("\n".join(set_blib))

with open(msgfplus_peptide_file, "a") as f:
    f.write("\n".join(set_msgfplus))

with open(matched_peptide_file, "a") as f:
    f.write("\n".join(set_matched))