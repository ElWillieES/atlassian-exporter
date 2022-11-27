import datetime
import csv

def get_json_to_list(json_data, key_list):
    tmp_list = []
    for key in key_list:
        tmp_list.append(json_data[key])

    return tmp_list

def export_csv(export_filename, rows_list, header_list, key_list):
    print("{} - INFO - Exporting data to {}".format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), export_filename))
    with open(export_filename, mode='w',encoding='utf-8') as file:
        file = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        file.writerow(header_list)
        for row in rows_list:
            file.writerow(get_json_to_list(row, key_list))
