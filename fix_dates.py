# !/usr/bin/python
import os
from PIL.ExifTags import TAGS

import sys
import re
import datetime
from pexif import JpegFile

TIME_FORMAT = '%Y:%m:%d %H:%M:%S'

DRY_RUN = len(sys.argv) == 3 and sys.argv[2] == 'dr'
DEBUG = False

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


def get_exif_info(file):
    exif = file.get_exif(create=True)

    if DEBUG:
        file.dump()

    if exif:
        primary = exif.get_primary()

    if exif is None or primary is None:
        primary = {}

    return primary

def fix_file_date(file, file_path, exif_info, new_date):
    date_to_use = new_date.strftime(TIME_FORMAT)

    exif_info.DateTime = date_to_use
    exif_info.ExtendedEXIF.DateTimeOriginal = date_to_use
    exif_info.ExtendedEXIF.DateTimeDigitized = date_to_use

    if DRY_RUN == False:
        print('    Saving file...')
        try:
            file.writeFile(file_path)
        except IOError:
            type, value, traceback = sys.exc_info()
            print >> sys.stderr, "Error saving %s:" % file_path, value


def file_needs_date_fix(exif_info):
    dateTime = None
    try:
        dateTime = exif_info.DateTime
    except AttributeError:
        pass

    dateTime_original = None
    try:
        dateTime_original = exif_info.ExtendedEXIF.DateTimeOriginal
    except AttributeError:
        pass

    dateTime_digitized = None
    try:
        dateTime_digitized = exif_info.ExtendedEXIF.DateTimeDigitized
    except AttributeError:
        pass

    return dateTime is None and dateTime_original is None and dateTime_digitized is None;


def check_folder(folder):
    for root, sub_folders, files in os.walk(folder):
        print('* ' + root)

        for sub_folder in sub_folders:
            check_folder(sub_folder)

        if len(files):
            folder_name_date = get_date_from_path(root)

        for filename in files:
            if filename.lower().endswith('.jpg'):
                file_path = os.path.join(root, filename)

                pexif_file = JpegFile.fromFile(file_path)
                exif = get_exif_info(pexif_file)
                if file_needs_date_fix(exif):
                    print('  image: ' + file_path)
                    print('    FIX TO DATE = ' + folder_name_date.strftime("%Y/%m/%d"))
                    fix_file_date(pexif_file, file_path, exif, folder_name_date)


# --------
# Main
# --------

base_folder = sys.argv[1]

def main():
    print('base_folder = ' + base_folder + ' (' + os.path.abspath(base_folder) + ')')

    check_folder(base_folder)

    return 0

if __name__ == "__main__":
    sys.exit(main())
