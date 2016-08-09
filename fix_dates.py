# !/usr/bin/python
import os
import sys
import re
import datetime
from gi.repository import GExiv2

DRY_RUN = len(sys.argv) == 3 and sys.argv[2] == 'dr'

if DRY_RUN:
    print('######################################')
    print('This is dry run. Not changing any file')
    print('######################################')


# --------
# Methods
# --------

def get_date_from_path(path):
    folder_name = os.path.basename(path)

    date_re = re.search('.*/([0-5][0-9][0-5][0-9])/([0-5][0-9]).*', path)

    if date_re:
        year_number = date_re.group(1)
        month_number = date_re.group(2)
        return datetime.date(int(year_number), int(month_number), 1)
    else:
        return 'N/A'


def fix_file_date(exif_info, new_date):
    exif_info['Exif.Image.DateTime'] = new_date
    exif_info['Exif.Photo.DateTimeDigitized'] = new_date
    exif_info['Exif.Photo.DateTimeOriginal'] = new_date

    if DRY_RUN == False:
        exif_info.save_file()


def file_needs_date_fix(exif_info):
    date_time = exif_info.get_date_time()

    return date_time is None


def check_folder(folder):
    for root, sub_folders, files in os.walk(folder):
        print('\n#########\nfolder = ' + root)

        for sub_folder in sub_folders:
            check_folder(sub_folder)

        if len(files):
            folder_name_date = get_date_from_path(root)

        for filename in files:
            if filename.lower().endswith('.jpg'):
                file_path = os.path.join(root, filename)

                print('  image: ' + file_path)
                exif_info = GExiv2.Metadata()
                exif_info.open_path(file_path)
                if file_needs_date_fix(exif_info):
                    print('    FIX TO DATE = ' + folder_name_date.strftime("%Y/%m/%d"))
                    fix_file_date(exif_info, folder_name_date)


# --------
# Main
# --------

base_folder = sys.argv[1]

print('base_folder = ' + base_folder + ' (' + os.path.abspath(base_folder) + ')')

check_folder(base_folder)
