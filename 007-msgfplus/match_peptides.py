import os
import pandas as pd
import regex
from pandas.core.common import intersection

path = os.getcwd()
input_path = path + "\\input\\"
output_path = path + "\\output\\"
result_out_path = '{0}msgfp_v2\\'.format(output_path)

# msgfdb_tsv = '{0}KO_RPick_02_23_LTQ_2_24Feb06_Sphinx_06-01-07_msgfdb_fht.txt'.format(input_path)
blib_tsv = '{0}Ralstonia_pickettii.blib.tsv'.format(input_path)
merged_msgfplus_tsv = '{0}KO_Rpick_Merged_I.tsv'.format(result_out_path)
msgfplus_peptide_filtered_file = '{0}KO_Rpick_Merged_I_qfilter_0.0001.txt'.format(result_out_path)

result_file = '{}matched_pepdtide_results.txt'.format(result_out_path)
blib_peptide_file = '{}Ralstonia_pickettii.blib.peptides.txt'.format(result_out_path)
msgfplus_peptide_file = '{}KO_Rpick_Merged_MsgfPlus.peptides.txt'.format(result_out_path)
matched_peptide_file = '{}blib_msgfplus_matched_peptides.txt'.format(result_out_path)
unmatched_peptide_file = '{}blib_msgfplus_unmatched_peptides.txt'.format(result_out_path)
qfilter_matched_peptide_file = '{}blib_msgfplus_qfilter_matched_peptides.txt'.format(result_out_path)
qfilter_unmatched_peptide_file = '{}blib_msgfplus_qfilter_unmatched_peptides.txt'.format(result_out_path)
unmatched_overlaps_peptide_file = '{}msgfplus_unmatched_overlap_peptides.txt'.format(result_out_path)


# df_msgfdb = pd.read_table(msgfdb_tsv)

df_blib = pd.read_table(blib_tsv)
df_msgfplus = pd.read_table(merged_msgfplus_tsv)
# df_msgfplus_i = df_msgfplus.replace(['L'], ['I'])
# writer = pd.ExcelWriter(merged_msgfplus_i_tsv)
# df_msgfplus_i.to_excel(writer,'Sheet1')
# writer.save()
# writer.close()

# list_peptide_msgfdb = df_msgfdb['Peptide'].tolist()
list_peptide_blib = df_blib['peptideSeq'].tolist()
list_peptide_blib = [pep.replace('L','I') for pep in list_peptide_blib]
list_peptide_msgfplus = df_msgfplus['Peptide'].tolist()
list_peptide_msgfplus_qfilter = []

with open(msgfplus_peptide_filtered_file) as file:
    for line in file.read().splitlines():
        list_peptide_msgfplus_qfilter.append(line)


# set_msgfdb = set(list_peptide_msgfdb)
set_blib = set(list_peptide_blib)
set_msgfplus_fixed = set()
set_msgfplus = set(list_peptide_msgfplus)
set_msgfplus_qfilter = set(list_peptide_msgfplus_qfilter)

for msgf_pep in set_msgfplus:
    match = regex.search(r'\.{1}.+\.', msgf_pep)
    if match:
        pep_seq = match.group(0)
        reg_pattern = regex.compile('[^a-zA-Z]')
        pep_seq = reg_pattern.sub('', pep_seq)
        set_msgfplus_fixed.add(pep_seq)

set_matched = intersection(set_blib, set_msgfplus_fixed)
set_matched_qfilter = intersection(set_blib, set_msgfplus_qfilter)

set_unmatched = set(set_blib).symmetric_difference(set_msgfplus_fixed)
set_unmatched_qfilter = set(set_blib).symmetric_difference(set_msgfplus_qfilter)

with open(result_file, "w") as result:
    # result.write(('all peptide count in msgfdb database : {0}\n'.format(list_peptide_msgfdb.__len__())))
    result.write(('all peptide count in blib database : {0}\n'.format(list_peptide_blib.__len__())))
    result.write(('all peptide count in msgfplus merged database : {0}\n'.format(list_peptide_msgfplus.__len__())))
    # result.write(('unique peptide count in msgfdb database : {0}\n'.format(set_msgfdb.__len__())))
    result.write(('unique peptide count in blib database : {0}\n'.format(set_blib.__len__())))
    result.write(('unique peptide count in msgfplus merged database : {0}\n'.format(set_msgfplus_fixed.__len__())))
    result.write(('unique peptide count in msgfplus qfilter database : {0}\n'.format(set_msgfplus_qfilter.__len__())))
    result.write(('unique peptide matched count for msgfplus merged-blib : {0}\n'.format(set_matched.__len__())))
    result.write(('unique peptide matched count for msgfplus qfilter-blib : {0}\n'.format(set_matched_qfilter.__len__())))

with open(blib_peptide_file, "w") as f:
    f.write("\n".join(set_blib))

with open(msgfplus_peptide_file, "w") as f:
    f.write("\n".join(set_msgfplus_fixed))

with open(matched_peptide_file, "w") as f:
    f.write("\n".join(set_matched))

with open(qfilter_matched_peptide_file, "w") as f:
    f.write("\n".join(set_matched_qfilter))

with open(unmatched_peptide_file, "w") as f:
    f.write("\n".join(set_unmatched))

with open(qfilter_unmatched_peptide_file, "w") as f:
    f.write("\n".join(set_unmatched_qfilter))

set_unmatched_overlaps = intersection(set_unmatched, set_unmatched_qfilter)
with open(unmatched_overlaps_peptide_file, "w") as f:
    f.write("\n".join(set_unmatched_overlaps))