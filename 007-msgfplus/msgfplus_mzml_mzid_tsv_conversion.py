import glob
import os
import subprocess
import utility

path = os.getcwd()
input_path = path + "\\input\\"
output_path = path + "\\output\\"
java_exec_path = 'C:\\Program Files\\Java\\jre1.8.0_112\\bin\\java.exe'
msgfplus_jar_path = 'D:\\Server\\MSGFPlus\\MSGFPlus.jar'
mzml_path = 'D:\\Ralstonia_pickettii'
msgfp_mods_file_path = '{0}MSGFPlus_Mods-20161121.txt'.format(input_path)
db_fasta_file_path = '{0}ID_004956_793E1036.fasta'.format(input_path)
out_result_folder = "{0}msgfp_v3".format(output_path)

mzid_to_tsv_exec_path = 'D:\\Server\\MSGFPlus\\MzidToTsvConverter\\MzidToTsvConverter.exe'

mzml_mzid_cmd = '"{java_exec_path}" -Xmx4000M ' \
                '-jar "{msgfplus_jar_path}" ' \
                '-s "{mzml_path}\\{filename}.mzML" ' \
                '-o "{out_result_folder}\\{filename}.mzid" ' \
                '-d "{db_fasta_file_path}" ' \
                '-t 2.5Da,1.5Da -m 0 -inst 0 -e 1  -ntt 1 -tda 1 -minLength 6 '\
                '-maxLength 50 -minCharge 2 -maxCharge 5 -n 1 -thread 8 ' \
                '-mod "{msgfp_mods_file_path}"'

mzid_tsv_cmd_win = '{mzid_to_tsv_exec_path} ' \
               '-mzid:"{input_folder}\\{filename}.mzid" ' \
               '-tsv:"{output_folder}\\{filename}.tsv"'

mzid_tsv_cmd = '"{java_exec_path}" -Xmx3500M ' \
               '-cp "{msgfplus_jar_path}" edu.ucsd.msjava.ui.MzIDToTsv ' \
               '-i "{input_folder}\\{filename}.mzid" ' \
               '-o "{output_folder}\\{filename}.tsv" '

tsv_file_merged = '{0}\\KO_Rpick_Merged.tsv'.format(out_result_folder)
list_tsv_files = []
list_ignore = []

for file in glob.glob(os.path.join(out_result_folder, '*.mzid')):
    filenameext = os.path.basename(file)
    filename = os.path.splitext(filenameext)[0]
    list_ignore.append(filename)

for file in glob.glob(os.path.join(mzml_path, '*.mzML')):
    filenameext = os.path.basename(file)
    filename = os.path.splitext(filenameext)[0]
    if filename not in list_ignore:
        subprocess.call(mzml_mzid_cmd.format(java_exec_path = java_exec_path,
                                             msgfplus_jar_path = msgfplus_jar_path,
                                             mzml_path = mzml_path,
                                             db_fasta_file_path = db_fasta_file_path,
                                             out_result_folder = out_result_folder,
                                             msgfp_mods_file_path = msgfp_mods_file_path,
                                             filename = filename), shell=True)

for file in glob.glob(os.path.join(mzml_path, '*.mzML')):
    filenameext = os.path.basename(file)
    filename = os.path.splitext(filenameext)[0]
    subprocess.call(mzid_tsv_cmd.format(mzid_to_tsv_exec_path = mzid_to_tsv_exec_path,
                                        input_folder = out_result_folder,
                                        output_folder = out_result_folder,
                                        filename = filename), shell=True)

for file in glob.glob(os.path.join(out_result_folder, '*.tsv')):
    list_tsv_files.append(file)

utility.concat_files(list_tsv_files, tsv_file_merged, True)

# subprocess.call('ren *.txt *.bat', shell=True)