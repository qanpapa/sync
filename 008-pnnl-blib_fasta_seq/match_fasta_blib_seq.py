import os
import glob
import fnmatch
from Bio import SeqIO

path = os.getcwd()
input_path = path + "\\input\\"
output_path = path + "\\output\\"

fasta = '{0}ID_004956_793E1036.fasta'.format(input_path)
unip_fasta = '{0}uniprot_seq_ralstonia_pickettii.fasta'.format(input_path)
unk_unm_unip_fasta = '{0}ralstonia_pickettii_unip_seq_unm_unk.fasta'.format(input_path)
uniprot_seq_merged_fasta = '{0}uniprot_seq_merged.fasta'.format(input_path)
pnnl_blib_tsv = '{0}Ralstonia_pickettii.blib.tsv'.format(input_path)
result_file = '{0}results.txt'.format(output_path)

list_pept = []

def increase_dict_val(dict, key, val):
    if key not in dict:
        dict[key] = val
    else:
        dict[key] += val


def calc_peptide_matches(fasta_seq_list, fasta_filename):
    list_prot = []
    dict_occur_matrix = {}
    dict_count_matrix = {}
    dict_occur_matrix_prot = {}
    dict_count_matrix_prot = {}
    dict_occur_matrix_pept = {}
    dict_count_matrix_pept = {}

    all_pep_count = 0
    all_pept_occur = 0
    for record in fasta_seq_list:
        prot = record.seq
        list_prot.append(prot)
        prot_index = list_prot.__len__() - 1
        pept_index = 0
        prot_pept_occur = 0

        for pept in list_pept:
            pept_occur = prot.count(pept)

            if pept_occur > 0:
                prot_pept_occur += pept_occur
                # all_pept_occur += pept_occur

                cross_index = '{0}_{1}'.format(prot_index, pept_index)
                cross_prot_index = '{0}'.format(prot_index)
                cross_pept_index = '{0}'.format(pept_index)

                dict_occur_matrix[cross_index] = pept_occur
                dict_occur_matrix_prot[cross_prot_index] = prot_pept_occur
                increase_dict_val(dict_occur_matrix_pept, cross_pept_index, pept_occur)

                increase_dict_val(dict_count_matrix, cross_index, 1)
                increase_dict_val(dict_count_matrix_prot, cross_prot_index, 1)
                increase_dict_val(dict_count_matrix_pept, cross_pept_index, 1)

            pept_index += 1

    sum_peptide_count = sum(dict_count_matrix_pept.values())
    sum_peptide_occurrence = sum(dict_occur_matrix_pept.values())

    with open(result_file, "a") as result:
        result.write(('all protein sequence count in fasta: {1} database: {0}\n'.format(dict_count_matrix_prot.__len__(), fasta_filename)))
        result.write('all peptides count in blib database: {0}\n'.format(list_pept.__len__()))
        result.write('number of unique peptides matched with fasta: {0} database: {1}\n'.format(fasta_filename, dict_count_matrix_pept.__len__()))
        result.write('all peptides count matched with fasta: {0} database: {1}\n'.format(fasta_filename, sum_peptide_count))
        result.write('all peptides occurrence matched with fasta: {0} database: {1}\n\n'.format(fasta_filename, sum_peptide_occurrence))

    # print('all protein sequence count in fasta database: {0}'.format(dict_count_matrix_prot.__len__()))
    # print('all peptides count in blib database: {0}'.format(list_pept.__len__()))
    # print('number of unique peptides matched with fasta{0} database: {1}'.format(fasta_filename, dict_count_matrix_pept.__len__()))
    # print('all peptides count matched with fasta{0} database: {1}'.format(fasta_filename, sum_peptide_count))
    # print('all peptides occurrence matched with fasta{0} database: {1}'.format(fasta_filename, sum_peptide_occurrence))

    # dict_xls(dict_count_matrix_pept, '{0}_pept_occurrence.xlsx'.format(fasta_filename))
    # dict_xls(dict_occur_matrix_pept, '{0}_pept_count.xlsx'.format(fasta_filename))
    # dict_xls(dict_count_matrix, '{0}_occurrence.xlsx'.format(fasta_filename))
    # dict_xls(dict_occur_matrix, '{0}_count.xlsx'.format(fasta_filename))

with open(pnnl_blib_tsv, "r") as blib:
    first_line = True
    for bline in blib:
        if first_line:
            first_line = False
            continue
        splitted = bline.split('\t')
        b_seq = splitted[1]
        list_pept.append(b_seq)

fasta_seq_list = SeqIO.parse(open(fasta), 'fasta')
calc_peptide_matches(fasta_seq_list, 'ID_004956_793E1036')

fasta_seq_list = SeqIO.parse(open(unip_fasta), 'fasta')
calc_peptide_matches(fasta_seq_list, 'uniprot_seq_ralstonia_pickettii')

fasta_seq_list = SeqIO.parse(open(unk_unm_unip_fasta), 'fasta')
calc_peptide_matches(fasta_seq_list, 'ralstonia_pickettii_unip_seq_unm_unk')


# fasta_files = [unip_fasta, uniprot_seq_merged_fasta]
#
# with open(uniprot_seq_merged_fasta, 'w') as w_file:
#     for fasta in fasta_files:
#         with open(fasta, 'rU') as o_file:
#             seq_records = SeqIO.parse(o_file, 'fasta')
#             SeqIO.write(seq_records, w_file, 'fasta')


# pattern = '*='
# matching = fnmatch.filter(dict_count_matrix, pattern)
# if matching:
#     for m in matching:
#         print(dict_count_matrix[m])

# pattern = spc + '*'
# matching = fnmatch.filter(listOrganisms, pattern)
# if matching:
#     for m in matching:
#         listMatching.append(m)

