import sys
import os
import pathlib
import datetime
import csv
import re
import urllib.error
import urllib.request

"""
CSVに記載されている画像URLを取得し、ディレクトリに保存するプログラム。
"""

__auther__ = 'NAOKI OKAMOTO'
__version__ = '0.1.0'
__date__ = '2020/01/24'

DIRECTORY_WIDTH = 2

def get_params():

    # input and check file is.
    csv_file_path = ''
    while True:
        print('input file path?')
        csv_file_path = input()

        if csv_file_path == 'exit()':
            sys.exit(-1)
        
        f = pathlib.Path(csv_file_path)

        if f.is_file():
            break
        
        print('that is not a file path. type again')
    

    # input nand check directory is
    output_directory_path = ''
    current_directory = os.getcwd()

    while True:
        print('output directory? (brank means ' + current_directory + ')')
        output_directory_path = input()

        if output_directory_path == 'exit()':
            sys.exit(-1)

        if output_directory_path == '':
            output_directory_path = '.'
        
        p = pathlib.Path(output_directory_path)

        if p.is_dir():
            break
        
        print('that is not a directory path. type again')

    # input ignore lines
    print('ignore lines? (split with space, start with 1)')
    ignore_lines_str = input()

    if ignore_lines_str == 'exit()':
        sys.exit(-1)

    ignore_lines = []

    for each in ignore_lines_str.split():
        ignore_lines.append(int(each))

    return (csv_file_path, output_directory_path, ignore_lines)

def read_csv(csv_file_path, output_directory_path, ignore_lines):

    csv_file = pathlib.Path(csv_file_path)
    dt = datetime.datetime.now()
    datetime_str = str(dt.year) + "_" + str(dt.month) + "_" + str(dt.day) + "_" + str(dt.hour) + "_" + str(dt.minute) + "_" + str(dt.second)
    output_directory_path = output_directory_path + '/file download ' + datetime_str
    output_directory = pathlib.Path(output_directory_path)
    output_directory.mkdir()

    middle_dir = output_directory
    last_dir = middle_dir
    current_line = 1


    # 以下整理したい. 階層に対して深さ優先探索にする
    with csv_file.open(encoding='utf8') as csv_file:
        csv_data = csv.reader(csv_file)
        for each_line in csv_data:
            pass_mode = False
            if not contains(current_line, ignore_lines):
                directory_depth = DIRECTORY_WIDTH
                for each_comp in each_line:
                    if directory_depth is 2:
                        directory_depth -= 1
                        if each_comp != '':
                            middle_dir = pathlib.Path(str(output_directory) + '/' + each_comp)
                            middle_dir.mkdir()
                    elif directory_depth is 1:
                        last_dir = pathlib.Path(str(middle_dir) + '/' + each_comp)
                        last_dir.mkdir()
                        directory_depth -= 1
                    elif directory_depth is 0:
                        if 'http' in each_comp:
                            url_splits = each_comp.split('/')
                            img_id = get_url_id(url_splits)
                            img_url = get_google_download_link(img_id)
                            file_downloader(img_url, str(last_dir))
                            
            current_line += 1

def file_downloader(url, path):
    try:
        with urllib.request.urlopen(url) as web_file:
            header_split = str(web_file.info()).split()
            content_discription = header_split[header_split.index('Content-Disposition:')+1].split(';')[1]
            ATTRIBUTE = 'filename='
            file_name = content_discription[len(ATTRIBUTE):].strip('"')
            print('downloading... ' + file_name + ' from... ' + url + ' to... ' + str(path))
            with open(str(path) + '/' + file_name, 'wb') as local_file:
                local_file.write(web_file.read())
    except urllib.error.URLError as e:
        print(e)

def get_url_id(url_splits):
    if len(url_splits) > 3:
        if 'file' in url_splits:
            return url_splits[url_splits.index('file') + 2]
        elif 'drive' in url_splits:
            return url_splits[url_splits.index('drive') + 2]
        elif 'open' in url_splits[3]:
            return re.split('[?=&]', url_splits[3])[2]

def get_google_download_link(img_id):
    return 'https://drive.google.com/uc?id=' + img_id + ''

def contains(obj, objs):
    for each in objs:
        if obj == each:
            return True
    return False

def main():

    # file_downloader('https://drive.google.com/uc?id=1MHqqGKUB30mKMMXqWqhNrNNsWBPZIBJM', 'tmp')

    (csv_file_path, output_directory_path, ignore_lines) = get_params()
    
    read_csv(csv_file_path, output_directory_path, ignore_lines)

    return 0

if __name__ == '__main__':

    return_code = main()

    if return_code is None:
        return_code = 0

    sys.exit(return_code)