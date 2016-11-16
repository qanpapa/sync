import glob
import os
import subprocess
import utility

# input_path = 'E:\\Desktop\\test\\input'


mzml_path = 'F:\\MSV000079053_MZML\\Ralstonia_pickettii'
path = os.getcwd()
output_path = path + "\\output\\"

mzml_mzid_cmd = '"C:\\Program Files\\Java\\jre1.8.0_112\\bin\\java.exe" -Xmx4000M ' \
                '-jar "D:\\Server\\MSGFPlus\\MSGFPlus.jar" ' \
                '-s "F:\\MSV000079053_MZML\\Ralstonia_pickettii\\{0}.mzML" ' \
                '-o "F:\\Proteomics\\007-msgfplus\\output\\{0}.mzid" ' \
                '-d "F:\\Proteomics\\007-msgfplus\\input\\ID_004956_793E1036.fasta" ' \
                '-t 0.5Da -m 1 -inst 0 -e 1  -ntt 0 -tda 1 -minLength 6 -maxLength 40 -n 1 -thread 8 ' \
                '-mod "F:\\Proteomics\\007-msgfplus\\input\\MSGFPlus_Mods.txt"'

mzid_tsv_cmd = 'D:\\Server\\MSGFPlus\\MzidToTsvConverter\\MzidToTsvConverter.exe ' \
               '-mzid:"F:\\Proteomics\\007-msgfplus\\output\\{0}.mzid" ' \
               '-tsv:"F:\\Proteomics\\007-msgfplus\\output\\{0}.tsv"'

tsv_file_merged = '{0}KO_Rpick_Merged.tsv'.format(output_path)
list_tsv_files = []
list_ignore = []

for file in glob.glob(os.path.join(output_path, '*.mzid')):
    filenameext = os.path.basename(file)
    filename = os.path.splitext(filenameext)[0]
    list_ignore.append(filename)

for file in glob.glob(os.path.join(mzml_path, '*.mzML')):
    filenameext = os.path.basename(file)
    filename = os.path.splitext(filenameext)[0]
    if filename not in list_ignore:
        subprocess.call(mzml_mzid_cmd.format(filename), shell=True)

for file in glob.glob(os.path.join(mzml_path, '*.mzML')):
    filenameext = os.path.basename(file)
    filename = os.path.splitext(filenameext)[0]
    subprocess.call(mzid_tsv_cmd.format(filename), shell=True)

for file in glob.glob(os.path.join(output_path, '*.tsv')):
    list_tsv_files.append(file)

utility.concat_files(list_tsv_files, tsv_file_merged, True)

# subprocess.call('ren *.txt *.bat', shell=True)