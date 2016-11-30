import regex

from utility import get_dir_file_list
from os import getcwd

path = getcwd()
mzml_path = 'F:\\mzML_postRefinement_files\\'

output_path = path + "\\output\\"

file = '{0}mzml_file_list.tsv'.format(output_path)

set_species = set()
list_files = get_dir_file_list(mzml_path)

with open(file, "w") as f:
    for mzml_f in list_files:
        mzml_f = mzml_f.replace('Biodiversity_','')
        match = regex.search(r'^[a-zA-Z]+_[a-zA-Z]+', mzml_f)
        if match:
            specy = match.group(0)
            set_species.add(specy)

    f.write("\n".join(set_species))
