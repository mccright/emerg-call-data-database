import string

import pandas as pd
import csv
from re import compile, IGNORECASE
from pathlib import Path
import os
import types
import matplotlib.pyplot as plt
import datetime
import numpy
from sqlalchemy.ext.indexable import index_property


start = datetime.datetime.now()
dir_path = os.getcwd()
allowed_characters = set(r'{0}{1} []><()$%-_/., * $'.format(string.ascii_letters, string.digits))
# set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'))
separator = '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'


def read_csv_criticality_file(filename: Path, **csv_params: object) -> list[list[str]]:
    with open(filename, encoding='utf-8', newline='') as file:
        return list(csv.reader(file, **csv_params))


def read_csv_data_file(filename: str) -> csv.DictReader:
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        #csv_raw_data: csv.DictReader = read_csv_data_file(filename)
        num_columns = len(reader.fieldnames)  # Get the first row
        print(f"The number of columns in {filename} is: {num_columns}")
        return reader

def build_calltype_criticality_dict(filename: Path) -> dict:
    # Read CSV data into a csv object, list[list[str]]
    csv_raw_data = read_csv_criticality_file(filename)
    priority_dict = {}
    # if 'card' == a number
    # Match all numbers
    # + indicate 1 or more occurrences of \d
    digits_pattern: str = r'\d+'   #r"[1234567890]{1}"
    regex_pattern_digits_pattern = compile(digits_pattern)
    call_types_pattern: str = r'ACCLE|AIRCRASH|ALERT1|ALERT2|ALERT3|ALS|AMMO|ARSON|BOMB|C13F|CARFIRE|CODET|DUMPFIRE|ECHO|ELEVATOR|FFINJ|FIREA|FIREB|FIREC|FIREI|GASLEAK|GRASFIRE|GROUND|HAZ1|HAZ3|HAZ2|HAZ2I|HAZPKG|LIFTASST|MED|MEDA|MEDB|MEDC|MEDD|MEDE|MEDFD|MEDLE|MEDOA|MEDSD|MUTAID|NOEMD|ODOR|OMEGA|OMEGAD|PLAN|REFUEL|RSAlarm|SERVCALL|SPECDUTY|STANDBY|STILL|SUSPART|SWAT|TEST|WALKIN|WIRES'
    regex_pattern_call_types_pattern = compile(call_types_pattern, flags=IGNORECASE)
    for row in csv_raw_data:
        if regex_pattern_digits_pattern.match(row[1]):
            # lowercase all characters and remove whitespace
            this_key = f"{row[1].lower().strip()}{row[2].lower().strip()}{row[3].lower().strip()}{row[4].lower().strip()}"
            priority_dict.update({this_key: row[11].lower().strip()})
            ##determinant_description_dict.update({this_key: row[7].lower().strip()})
        elif regex_pattern_call_types_pattern.match(row[1].lower().strip()):
            # lowercase all characters and remove whitespace
            this_key = f"{row[1].lower().strip()}"
            priority_dict.update({this_key: row[11].lower().strip()})
    return priority_dict



def build_calltype_determinant_description_dict(filename: Path) -> dict:
    # Read CSV data into a csv object, list[list[str]]
    csv_raw_data = read_csv_criticality_file(filename)
    determinant_description_dict = {}
    # if 'card' == a number
    # Match all numbers
    # + indicate 1 or more occurrences of \d
    digits_pattern: str = r'\d+'   #r"[1234567890]{1}"
    regex_pattern_digits_pattern = compile(digits_pattern)
    call_types_pattern: str = r'ACCLE|AIRCRASH|ALERT1|ALERT2|ALERT3|ALS|AMMO|ARSON|BOMB|C13F|CARFIRE|CODET|DUMPFIRE|ECHO|ELEVATOR|FFINJ|FIREA|FIREB|FIREC|FIREI|GASLEAK|GRASFIRE|GROUND|HAZ1|HAZ3|HAZ2|HAZ2I|HAZPKG|LIFTASST|MED|MEDA|MEDB|MEDC|MEDD|MEDE|MEDFD|MEDLE|MEDOA|MEDSD|MUTAID|NOEMD|ODOR|OMEGA|OMEGAD|PLAN|REFUEL|RSAlarm|SERVCALL|SPECDUTY|STANDBY|STILL|SUSPART|SWAT|TEST|WALKIN|WIRES'
    regex_pattern_call_types_pattern = compile(call_types_pattern, flags=IGNORECASE)
    for row in csv_raw_data:
        if regex_pattern_digits_pattern.match(row[1]):
            # combine four columns and
            # lowercase all characters and remove whitespace
            this_key = f"{row[1].lower().strip()}{row[2].lower().strip()}{row[3].lower().strip()}{row[4].lower().strip()}"
            temp_determinant_desc = replace_invalid_characters(f"{row[7].lower().strip()}", allowed_characters, '~')
            determinant_description_dict.update({this_key: temp_determinant_desc})
        elif regex_pattern_call_types_pattern.match(row[1].lower().strip()):
            # lowercase all characters and remove whitespace
            this_key = f"{row[1].lower().strip()}"
            temp_determinant_desc = replace_invalid_characters(f"{row[7].lower().strip()}", allowed_characters, '~')
            determinant_description_dict.update({this_key: temp_determinant_desc})
    return determinant_description_dict


def replace_invalid_characters(input_string, allowed_chars, replacement):
    # Model from: https://www.geeksforgeeks.org/python/replacing-characters-in-a-string-using-dictionary-in-python/
    return ''.join(c if c in allowed_chars else replacement for c in input_string)


def build_calltype_criticality_match_dict(filename: Path, priority_dict: dict, determinant_description_dict: dict):
    # Read CSV data into a csv object, list[list[str]]
    # csv_raw_data: csv.DictReader = read_csv_data_file(filename)
    # with open(filename) as csvfile:
    # Model from:
    # https://dev.to/bowmanjd/flexible-csv-handling-in-python-with-dictreader-and-dictwriter-3hae
    # and
    # https://github.com/bowmanjd/pycsvdemo/
    with filename.open('r', newline='', encoding='utf-8') as csvfile:
        csv_raw_data = csv.DictReader(csvfile)
        num_columns = len(csv_raw_data.fieldnames)  # Get the first row
        rows = []
        print(f"The number of columns in \"{filename}\" is: {num_columns}")

        print(f"csv_raw_data type = {type(csv_raw_data)}")  # Confirm csv.DictReader type
        print(f" input header fields/columns: {csv_raw_data.fieldnames}") # Show column names
        found_counter: int = 0    # Track the matches
        missing_counter: int = 0  # Track those not found
        for row in csv_raw_data:
            incident_number = (row['incident_num'].lower().strip())
            incident_calltype = (row['call_type'].lower().strip())
            if incident_calltype in priority_dict:
                determinant_description = f"{determinant_description_dict[incident_calltype]}"
                sub_category = f"{priority_dict[incident_calltype]}"
                found_counter = found_counter + 1
            else:
                # CTNIMRS == Call Type not in Master Run Sheet.
                determinant_description = "CTNIMRS"
                sub_category = "CTNIMRS"
                missing_counter = missing_counter + 1
            new_row = {
                'incident_date': row['incident_date'],
                'incident_date_year_only': row['incident_date_year_only'],
                'incident_num': row['incident_num'],
                'response_unit': row['response_unit'],
                'response_level': row['response_level'],
                'call_type': incident_calltype,
                'sub_category': sub_category,
                'determinant_description': determinant_description,
                'dispatch_time': row['dispatch_time'],
                'dispatch_time_in_seconds': row['dispatch_time_in_seconds'],
                'enroute_time': row['enroute_time'],
                'enroute_time_in_seconds': row['enroute_time_in_seconds'],
                'arrive_time': row['arrive_time'],
                'arrive_time_in_seconds': row['arrive_time_in_seconds'],
                'response_time': row['response_time'],
                'response_time_in_seconds': row['response_time_in_seconds'],
                'time_in_service': row['time_in_service'],
                'time_in_service_in_seconds': row['time_in_service_in_seconds']
            }
            rows.append(new_row)


        print(f"{separator}")
        print(f"{found_counter} found")
        print(f"{missing_counter} missing")
        print(f"CTNIMRS == Call Type not in Master Run Sheet.")
        print(f"{separator}")

    return rows



def create_target_csv_data_file(csvfile_suffix: str) -> object:
    """Creates a path/file object with filename day-month-year

    Builds the filename with {date}_{csvfile_suffix}.
    Appends the filename to the current directory.
    :param csvfile_suffix: str
    :rtype: object
    """
    #
    filename_suffix = csvfile_suffix
    filename_prefix = start.strftime('%Y-%m-%d')
    filename = f"{filename_prefix}_{filename_suffix}"
    # Put the new file in the current directory
    csv_file_name: str = os.path.join(dir_path, filename)
    return csv_file_name



# Test dataset:
# './data/raw_criticality_sheet_test.csv'
# Full dataset:
# './data/110520_Master_Run_Sheet.csv'
#priorities_csv_file = './data/110520_Master_Run_Sheet.csv'
#test_emerg_call_data_csv_file = './data/test_input_file.csv'

csv_data_filename_suffix: str = 'emerg_data_organized_step_four.csv'
csv_data_filename: object = create_target_csv_data_file(csv_data_filename_suffix)

master_run_sheet_csv_file_path = Path("./data/110520_Master_Run_Sheet.csv")
test_emerg_call_data_csv_file_path = Path("./data/test_input_file.csv")
test_emerg_call_data_output_file_path = Path("./data/test_output_file.csv")
production_input_file = Path("./2025-08-01_add_response_time_columns_step_three.csv")
production_output_file = Path(str(csv_data_filename))
input_file = production_input_file
output_file = production_output_file

# Check the type of "master_run_sheet_csv_file_path"
#    print(f"{separator}")
#    print(f"master_run_sheet_csv_file_path type is {type(master_run_sheet_csv_file_path)}")
#
# For now, I view "Sub Category" as an indicator of "priority."
# So in this code, the "priorities" dictionary refers to mapping
# each call_type to its "Sub Category" from the "110520_Master_Run_Sheet.csv"
# build_calltype_criticality_dict() returns a dictionary
# characters lowercase and whitespace removed from all keys and values
priorities: dict = build_calltype_criticality_dict(master_run_sheet_csv_file_path)
determinant_descriptions: dict = build_calltype_determinant_description_dict(master_run_sheet_csv_file_path)
"""
At least 159 rows include "special" utf-8 characters that are SQL non-compliant
  For example: 
heart rate ��������� 50bpm and <130bpm (without priority symptoms)

hexdump -C
20 ef bf bd ef bf  bd ef bf bd 20
space
ef == Latin small letter i with diaeresis - ï
bf == Inverted question mark - ¿
bd == Fraction one half - ½
ef == Latin small letter i with diaeresis - ï
bf == Inverted question mark - ¿
bd == Fraction one half - ½
ef == Latin small letter i with diaeresis - ï
bf == Inverted question mark - ¿
bd == Fraction one half - ½
space

heart rate ï¿½ï¿½ï¿½ 50bpm and <130bpm (without priority symptoms)

# replace utf-8 character "�" with ascii "~"

# my_dict = {k: v.replace('world', 'Python') for k, v in my_dict.items()}
allowed_characters = string.ascii_letters + string.digits + r'()$%_/.,]*$'
for key, value in determinant_descriptions.items():
    value = ''.join(c for c in value if c in allowed_characters)

determinant_descriptions = {key: value.replace('ï', '~') for key, value in determinant_descriptions.items()}
determinant_descriptions = {key: value.replace('¿', '~') for key, value in determinant_descriptions.items()}
determinant_descriptions = {key: value.replace('½', '~') for key, value in determinant_descriptions.items()}
"""
print(f"{separator}")

new_file_rows = build_calltype_criticality_match_dict(input_file, priorities, determinant_descriptions)

# Write the processed data to a new CSV file
fieldnames = ['incident_date', 'incident_date_year_only', 'incident_num', 'response_unit', 'response_level', 'call_type', 'sub_category', 'determinant_description', 'dispatch_time', 'dispatch_time_in_seconds', 'enroute_time', 'enroute_time_in_seconds', 'arrive_time', 'arrive_time_in_seconds', 'response_time', 'response_time_in_seconds', 'time_in_service', 'time_in_service_in_seconds']
with open(output_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(new_file_rows)

num_columns = len(writer.fieldnames)  # Get the first row
print(f"The number of columns in \"{output_file}\" is: {num_columns}")
print(f"output header fields/columns: {writer.fieldnames}")  # Show column names

print(f"Data processing complete. ")
print(f"Input file is \"{input_file}\".")
print(f"Result saved in \"{output_file}\".")

