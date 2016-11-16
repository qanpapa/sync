import os
import glob
from datetime import datetime


def make_dir(dir_path):
    directory = os.path.dirname(dir_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_run_path():
    path = os.getcwd()
    return path


def get_time_now():
    now = datetime.now()
    date_now = '{}-{}-{}-{}-{}-{}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second)
    return date_now


def concat_files(list_files, new_file, files_include_header = False):
    with open(new_file, 'w') as new_f:
        if files_include_header:
            with open(list_files[0], 'r') as f:
                first_line = f.readline()
            new_f.write(first_line)

            for file_f in list_files:
                is_first_line = True
                f = open(file_f, 'r')
                for line in f:
                    if is_first_line:
                        is_first_line = False
                        continue
                    else:
                        new_f.write(line)
                f.close()  # y
        else:
                for file_path in list_files:
                    with open(file_path) as infile:
                        for line in infile:
                            new_f.write(line)


def dict_xls(dct, filename):
    import xlsxwriter

    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    row = 0
    col = 0

    for key in dct.keys():
        worksheet.write(row, col, key)
        worksheet.write(row, col + 1, dct[key])
        row += 1

    workbook.close()

def make_items_distinct_in_file(path=get_run_path(), filename_in='', sort=False,
                                prefix_or_postfix=0, fix_phrase=''):

    """Make distinct items in file or files.

        Keyword arguments:
        path                -- input & output directory (default working_dir)
        filename_in         -- filename to process or blank for all files in 'path' (default '')
        filename_out        -- filename to write or blank for all files in 'path' w/add prefix_or_postfix (default '')
        sort                -- if items to be sorted when writing them to file (default False)
        prefix_or_postfix   -- output filename prefix(1) OR postfix(2) (default 0)
        fix_phrase          -- output filename fix phrase (default '')
        """

    set_items = set()

    if path[len] != '/':
        path += '/'

    # if filename_out:
    #     out_file_path = path + filename_out

    if filename_in:
        in_file_path = path + filename_in

        with open(in_file_path) as file:
            for line in file.read().splitlines():
                set_items.add(line)
    else:
        for filename in glob.glob(os.path.join(path)):
            with open(filename) as file_x:
                for line in file_x:
                    set_items.add(line)

    def make_distinct_file(file_name):
        with open(file_name) as f:
            for f_line in f.read().splitlines():
                set_items.add(f_line)

    def make_merged_distinct_file(dir_path):
        for file_x in glob.glob(os.path.join(dir_path)):
            with open(filename) as file_x:
                for x_line in file_x:
                    set_items.add(x_line)

    if set_items.__len__() > 0:
        with open(out_file_path, "w") as file_out:
            if sort:
                list_sorted = sorted(set(set_items))
                file_out.write("\n".join(list_sorted))
            else:
                file_out.write("\n".join(set_items))
