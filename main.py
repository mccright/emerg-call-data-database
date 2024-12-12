# This is a rough problem-solving script.
# I knew almost nothing about the data and needed to poke at it 
#    for a while.  The *_time columns are a mess.
#  incident_date --> remove bogus time, convert date to pd.date
#  response_level
#  call_type --> See: https://en.wikipedia.org/wiki/Medical_Priority_Dispatch_System
#  Unit_Dispatch_Times --> isolate "team" and "time" components
#  Unit_Enroute_Times --> isolate "team" and "time" components
#  Unit_Arrive_Times --> isolate "team" and "time" components
#  Unit_At_Patient_Times --> isolate "team" and "time" components
#  Unit_Enroute_To_Hospital_Times --> isolate "team" and "time" components
#  Unit_Arrive_At_Hospital_Times --> isolate "team" and "time" components
#  Unit_Staging_Times --> isolate "team" and "time" components
#  Unit_Fire_Out_Times --> isolate "team" and "time" components
#  Unit_Clear_Times --> isolate "team" and "time" components
#  Time_In_Service --> isolate "team" and "time" components

from pathlib import Path
# import ast
import sys
import os
import pandas as pd
import datetime
# import numpy as np
import pathlib
import tempfile
import string
import random
import logging
import shutil


# provide both local time and UTC time to better support
# distributed operations
start = datetime.datetime.now()
start_utc = datetime.datetime.now(datetime.timezone.utc)
dir_path = os.getcwd()

_LOGGER = logging.getLogger(__name__)


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


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def minimum_py(min_python_major_version=3, min_python_minor_version=10):
    # Use a breakpoint in the code line below to debug your script.
    if sys.version_info < (int(min_python_major_version), int(min_python_minor_version)):
        raise Exception("Use only with Python {min_python_major_version}.{min_python_minor_version} or higher")
    else:
        return True


def print_separator_line() -> str:
    print_separator = f'- - - - - - - - - - - - - - - - - - - - - - - -'
    return print_separator


def report_start(dirpath: str) -> str:
    """Documenting the report start time.

    Provides both local time and UTC time for distributed operations.
    Assumes "start" and "start_utc" are set at the top of the script.
    :param dirpath: root of target filesystem
    :type  dirpath: str
    :return report_start_msg: start of report message content
    """
    report_start_msg = f"\n\n{print_separator_line()}\n"
    report_start_msg = report_start_msg + f"{__file__}\n"
    report_start_msg = report_start_msg + f"Report started at: {start} local, {start_utc} UTC\n"
    report_start_msg = report_start_msg + f"Root of target filesystem: {dirpath}\n"
    report_start_msg = report_start_msg + f"{print_separator_line()}"
    return report_start_msg


def report_end(csvfile: str) -> str:
    """Documenting the report end time.

    "csvfile" is .
    Provides both local time and UTC time for distributed operations.
    :param csvfile: the report's full path + filename
    :type csvfile: str
    :return report_end_msg: end of report message content
    """
    # print(f"len(temp_data_frame_w_dates) = {length}")
    script_ended = datetime.datetime.now()
    script_ended_utc = datetime.datetime.now(datetime.timezone.utc)
    report_end_msg = f"\n\n{print_separator_line()}\n"
    report_end_msg = report_end_msg + f"{__file__}\n"
    report_end_msg = report_end_msg + f"Report started at: {start} local, {start_utc} UTC\n"
    report_end_msg = report_end_msg + f"Report ended at: {script_ended} local, {script_ended_utc} UTC\n"
    report_end_msg = report_end_msg + f"Report took: {(script_ended - start)}\n"
    report_end_msg = report_end_msg + f"Reporting processed {length} input records and output {outputfilelength} records\n"
    report_end_msg = report_end_msg + f"Report Output Files: {csvfile}\n"
    report_end_msg = report_end_msg + f"{print_separator_line()}"
    return report_end_msg


def data_description(data_frame):
    # Overview of the data:
    print_separator_line()
    print(f'Overview of the data {data_frame.info()}')
    print_separator_line()
    # How many rows & columns are there?
    print(f'There are {data_frame.shape[0]} records and {data_frame.shape[1]} columns in {e_data_file}')
    print_separator_line()
    # What are the column names & types?
    print(f'Column names and Python data types include: ')
    for column_name in data_frame.columns:
        print(f'\t{column_name} type is {data_frame.dtypes[column_name]}')
    print_separator_line()


def convert_column_to_date(data_frame):
    for index in data_frame.index:
        # Remove the bogus time from the incident_date column
        temp_incident_date = f"{data_frame.loc[index, 'incident_date']}"
        data_frame.loc[index, 'incident_date'] = temp_incident_date.split(' ', 1)[0]
        # data_frame.loc[index, 'incident_date'] = pd.to_datetime(data_frame.loc[index, 'incident_date']) # # datetime.datetime.strptime(data_frame.loc[index, 'incident_date'], "%m/%d/%y")
        # print(f'Overview of the data {data_frame.info()}')
        # print(f"{(data_frame.loc[index, 'incident_date']).strftime('%d/%m/%y')}")
        # print(f"{(data_frame.loc[index, 'incident_date'])}")
        # print(f"{type(data_frame.loc[index, 'incident_date'])}")
        # print(temp_incident_date_slice[0])
        # date[temp_incident_date_slice[0]] = datetime.strptime(date['incident_date'], "%Y-%m-%d hh:mm [am|pm]")
    # Convert the incident_date column to <class 'pandas._libs.tslibs.timestamps.Timestamp'>
    #   which is also datetime64[ns]
    # Either of the following approaches works, but pandas barks about it.
    # data_frame['incident_date'] = pd.to_datetime(data_frame['incident_date'])
    # Pandas issue helped parse the dates correctly:
    # https://github.com/pandas-dev/pandas/issues/52167
    # This is the second way:
    data_frame['incident_date'] = pd.to_datetime(data_frame.loc[:, 'incident_date'], format='mixed')
    # data_frame['incident_date'] = pd.to_datetime(data_frame.loc[:, 'incident_date'], date_format="%m/%d/%Y %I:%M:%S %p")
    # Check the data type:
    # print(f"{type(data_frame.loc[index,'incident_date'])}")
    # Sanity check the columns of data
    # print(f'Overview of the data {data_frame.info()}')
    return data_frame


"""
def convert_date_string_to_date(data_frame):
    # From: https://stackoverflow.com/questions/36753868/python-convert-dictionary-of-string-times-to-date-times
    dates = data_frame['incident_date']
    for date in dates:
        date['incident_date'] = datetime.strptime(date['incident_date'], "%Y-%m-%d hh:mm [am|pm]")
    data_description(data_frame)
"""


def get_only_dates(data_frame):
    dates = data_frame['incident_date']
    for date in dates:
        date.split(' ')


def file_write(path: str, data: any, mode: str = 'w'):
    with open(path, mode) as f:
        f.write(data)
        f.close()


def file_read(path: str, mode='r') -> any:
    with open(path, mode) as f:
        output = f.read()
        f.close()
    return output


def rand_temp_file() -> str:
    """
    Creates tempfile with a random-enough alpha-num name of given length.
    FROM: https://github.com/talhasch/aparat/blob/main/aparat/io.py
    """
    length = 16
    tf = os.path.join(tempfile.gettempdir(), random_alphanum(length) + '.tmp')
    file_write(tf, '')
    return tf


def random_alphanum(length: int) -> str:
    """
    Creates a random-enough alphanumeric string of given length.
    FROM: https://github.com/talhasch/aparat/blob/main/aparat/io.py
    """
    chars = string.ascii_letters + string.digits
    return ''.join((random.choice(chars)) for x in range(length))


def remove_tmp_file(tmpfile: str):
    try:
        # os.remove(tmpfile)
        # Reference: https://pynative.com/python-delete-files-and-directories/
        # approach below assumes Python 3.8 or above
        pathlib.Path(tmpfile).unlink(missing_ok=True)
        _LOGGER.info("Deleted file {}".format(tmpfile))
    except Exception as e:
        # this exception handling is only for dev & debugging
        print(f'{e}')
        _LOGGER.warning("Problem deleting file {}: Exception message: {}".format(tmpfile, e))
        pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(f"{report_start(dir_path)}")
    # Enforce a minimum Python version
    min_major_version = 3
    min_minor_version = 10
    minimum_py(min_major_version, min_minor_version)
    # Use a set: collection of unordered unique elements without duplicates {}
    emergency_data_list = []
    csv_data_filename_suffix: str = 'emerg_data_organized.csv'
    csv_data_filename: object = create_target_csv_data_file(csv_data_filename_suffix)
    # Get the source csv file and assign it to a dataframe called emergency_data
    # Enter the path to the raw data file here:
    ## e_data_file = Path("./data/rvfd-calls-for-service-Jan-2010.csv")
    e_data_file = Path("./data/rvfd-calls-for-service-2010-2020.csv")
    # Read the data into a Pandas dataframe
    if e_data_file.exists():
        emergency_data = pd.read_csv(e_data_file, sep=',')
    # replacing nan values in call_type, Unit_Dispatch_Times and Unit_Enroute_Times with "None"
    # From: https://www.geeksforgeeks.org/python-pandas-dataframe-fillna-to-replace-null-values-in-dataframe/
    # emergency_data["call_type"].fillna("None", inplace=True)
    # that approach is now aging out in favor of pandas 3.0 approach:
    # 'df.method({col: value}, inplace=True)' or df[col] = df[col].method(value) instead
    # This approach works:
    # emergency_data.fillna({"call_type": "None"}, inplace=True)
    emergency_data["call_type"] = emergency_data["call_type"].fillna("None")
    # Old way: emergency_data["Unit_Dispatch_Times"].fillna("None", inplace=True)
    # emergency_data.fillna({"Unit_Dispatch_Times": "None"}, inplace=True)
    emergency_data["Unit_Dispatch_Times"] = emergency_data["Unit_Dispatch_Times"].fillna("None")
    emergency_data["Unit_Enroute_Times"] = emergency_data["Unit_Enroute_Times"].fillna("None")
    emergency_data["Unit_Arrive_Times"] = emergency_data["Unit_Arrive_Times"].fillna("None")
    """
    print(f"{print_separator_line()}")
    print(f"{print_separator_line()}")
    print(f'Overview of the data {emergency_data.info()}')
    print(f"{print_separator_line()}")
    print(f"{print_separator_line()}")
    print(f'The data itself: {emergency_data}')
    print(f"{print_separator_line()}")
    print(f"{print_separator_line()}")
    """
    #
    # How many rows & columns are there? What are the column names & types?
    # data_description(emergency_data)
    # temp_data_frame = emergency_data.head(10)
    temp_data_frame = emergency_data
    # We need the .copy() below to stop Pandas from complaining with
    # "SettingWithCopyWarning" for the pd.to_datetime in convert_column_to_date()
    # See: https://stackoverflow.com/questions/71458707/pandas-settingwithcopywarning-for-pd-to-datetime
    temp_data_frame_w_dates = pd.DataFrame(convert_column_to_date(temp_data_frame.copy()))
    # print(f'Overview of the data {temp_data_frame_w_dates.info()}')
    # data_description(temp_data_frame)
    counter = 0
    length = len(temp_data_frame_w_dates)
    # print(f"len(temp_data_frame_w_dates) = {length}")
    while length > counter:
        # map each to a dictionary
        temp_values = ""
        # call_type is column 7
        call_type_dict = {}
        temp_str_call_type_dict = temp_data_frame_w_dates.values[counter][7]
        # stringified_call_type_times: str = ""
        # stringified_call_type_times = str(temp_str_call_type_dict)
        stringified_unit_dispatch_times: str = ""
        stringified_unit_enroute_times: str = ""
        stringified_unit_arrive_times: str = ""
        stringified_unit_time_in_service_times_dict: str = ""
        unit_dispatch_times_dict = {}
        unit_enroute_times_dict = {}
        unit_arrive_times_dict = {}
        unit_time_in_service_times_dict = {}
        # Unit_Dispatch_Times is column 8
        temp_str_unit_dispatch_dict = temp_data_frame_w_dates.values[counter][8]
        stringified_unit_dispatch_times = str(temp_str_unit_dispatch_dict)
        # Unit_Enroute_Times is column 9
        temp_str_unit_enroute_dict = temp_data_frame_w_dates.values[counter][9]
        stringified_unit_enroute_times = str(temp_str_unit_enroute_dict)
        temp_str_unit_arrive_dict = temp_data_frame_w_dates.values[counter][10]
        stringified_unit_arrive_times = str(temp_str_unit_arrive_dict)
        # Time_In_Service is column 17
        temp_str_unit_time_in_service_dict = temp_data_frame_w_dates.values[counter][17]
        stringified_unit_time_in_service_dict = str(temp_str_unit_time_in_service_dict)
        """
        # Up to four prints for debugging
        print(f"temp_str_unit_dispatch_dict = {temp_str_unit_dispatch_dict}")
        print(f"stringified_unit_dispatch_times = {stringified_unit_dispatch_times}")
        print(f"temp_str_unit_enroute_dict = {temp_str_unit_enroute_dict}")
        print(f"stringified_unit_enroute_times = {stringified_unit_enroute_times}")
        print(f"temp_str_unit_arrive_dict = {temp_str_unit_arrive_dict}")
        print(f"stringified_unit_arrive_times = {stringified_unit_arrive_times}")
        print(f"temp_str_unit_time_in_service_dict = {temp_str_unit_time_in_service_dict}")
        print(f"stringified_unit_time_in_service_dict = {stringified_unit_time_in_service_dict}")
        """
        #
        # Need data in the 'Unit_Dispatch_Times' column, the 8th column
        # 'Unit_Enroute_Times' column, the 9th column,
        # 'Unit_Arrive_Times' column, the 10th column and 
        # in the 'Time_In_Service column', the 17th column
        # Checking the numbered column for 'none' - not very portable :)
        if temp_data_frame_w_dates.values[counter][8] == "None" or temp_data_frame_w_dates.values[counter][9] == "None" or temp_data_frame_w_dates.values[counter][10] == "None" or temp_data_frame_w_dates.values[counter][17] == "None":
            # Skip the nulls
            counter += 1
            continue

        # We confirmed 'Unit_Dispatch_Time' and 'Time_In_Service' data
        else:
            # get 'response_unit=time' pairs from column 8 unit_dispatch_times
            try:
                unit_dispatch_times_dict = dict((a.strip(), b.strip())
                                                for a, b in (element.split('=')
                                                             for element in stringified_unit_dispatch_times.split(', ')))
                # print(f"DEBUG: unit_dispatch_times_dict is {str(unit_dispatch_times_dict)}")
            except Exception as e:
                print(f'{e}')
            # Now 9 - Unit_Enroute_Times
            try:
                unit_enroute_times_dict = dict((a.strip(), b.strip())
                                                for a, b in (element.split('=')
                                                             for element in stringified_unit_enroute_times.split(', ')))
                # print(f"DEBUG: unit_enroute_times_dict is {str(unit_enroute_times_dict)}")
            except Exception as e:
                print(f'Inside Unit_Enroute_Times: {e}')
            # Now 10 - Unit_Arrive_Times
            try:
                unit_arrive_times_dict = dict((a.strip(), b.strip())
                                                for a, b in (element.split('=')
                                                             for element in stringified_unit_arrive_times.split(', ')))
                # print(f"DEBUG: unit_arrive_times_dict is {str(unit_arrive_times_dict)}")
            except Exception as e:
                print(f'{e}')
            # Now 17
            try:
                unit_time_in_service_times_dict = dict((a.strip(), b.strip())
                                                for a, b in (element.split('=')
                                                             for element in stringified_unit_time_in_service_dict.split(', ')))
                # print(f"DEBUG: unit_time_in_service_times_dict is {str(unit_time_in_service_times_dict)}")
            except Exception as e:
                print(f'{e}')
            # Print what we learned for debugging
            print(f'Record: {counter}')
            # print("The resultant dictionary is: ", unit_dispatch_times_dict)
            # Now, for every unit dispatched, gather associated data and print it once record per row.
            for i in sorted(unit_dispatch_times_dict.keys()):

                if i != "None":
                    pass
                    # print(f"i = {i}")
                if temp_data_frame_w_dates.loc[counter, 'incident_date'] != "None":
                    pass
                    # print(f"{datetime.datetime.strftime(temp_data_frame_w_dates.loc[counter, 'incident_date'], '%m/%d/%y')}\t{i}")
                if i in unit_dispatch_times_dict and unit_dispatch_times_dict[i] != "None":
                    pass
                    # print(f"unit_dispatch_times -> {unit_dispatch_times_dict[i]}")
                if i in unit_enroute_times_dict and unit_enroute_times_dict[i] != "None":
                    pass
                    # print(f"unit_enroute_times -> {unit_enroute_times_dict[i]}")
                if i in unit_arrive_times_dict and unit_arrive_times_dict[i] != "None":
                    pass
                    # print(f"unit_arrive_times -> {unit_arrive_times_dict[i]}")
                if i in unit_time_in_service_times_dict and unit_time_in_service_times_dict[i] != "None":
                    pass
                    # print(f" time_in_service -> {unit_time_in_service_times_dict[i]}")
                #print(f"{datetime.datetime.strftime(temp_data_frame_w_dates.loc[counter, 'incident_date'], '%m/%d/%y')}\t{i} -> {unit_dispatch_times_dict[i]} -> {unit_enroute_times_dict[i]} -> {unit_arrive_times_dict[i]}   and time_in_service was {unit_time_in_service_times_dict[i]}")

                if (temp_data_frame_w_dates.loc[counter, 'call_type'], unit_dispatch_times_dict[i]):
                    if i in unit_dispatch_times_dict.values():
                        # continue
                        print(f"{datetime.datetime.strftime(temp_data_frame_w_dates.loc[counter, 'incident_date'], '%m/%d/%y')}\t{i} -> {unit_dispatch_times_dict[i]} -> {unit_enroute_times_dict[i]} -> {unit_arrive_times_dict[i]}   and time_in_service was {unit_time_in_service_times_dict[i]}")
                    # A team record must have each of dispatch, enroute, arrive, and time-in-service values in the original spreadsheet
                    if i in unit_enroute_times_dict:
                        if i in unit_arrive_times_dict:
                            if i in unit_time_in_service_times_dict:
                                # Known working, but wrong date format for SQLite
                                # csv_string = f"\"{datetime.datetime.strftime(temp_data_frame_w_dates.loc[counter, 'incident_date'], '%m/%d/%y')}\",\"{i}\",\"{temp_data_frame_w_dates.loc[counter, 'call_type'].strip()}\",\"{unit_dispatch_times_dict[i]}\",\"{unit_enroute_times_dict[i]}\",\"{unit_arrive_times_dict[i]}\",\"{unit_time_in_service_times_dict[i]}\"\n"
                                # Now using date format for SQLite: YYYY-MM-DD
                                csv_string = f"\"{datetime.datetime.strftime(temp_data_frame_w_dates.loc[counter, 'incident_date'], '%Y-%m-%d')}\",\"{i}\",\"{temp_data_frame_w_dates.loc[counter, 'call_type'].strip()}\",\"{unit_dispatch_times_dict[i]}\",\"{unit_enroute_times_dict[i]}\",\"{unit_arrive_times_dict[i]}\",\"{unit_time_in_service_times_dict[i]}\"\n"
                                emergency_data_list.append(csv_string)
                    #"""
                    # print(f"The type for {unit_dispatch_times_dict[i]} is {type(unit_dispatch_times_dict[i])}")
                    # diff = unit_dispatch_times_dict[i] + unit_time_in_service_times_dict[i]
                    # Print the difference in days, hours, minutes, and seconds
                    # print(f"The difference is {diff}")
                    # print("The resultant dictionary is: ", unit_dispatch_times_dict)
            counter += 1

    # Header row for csv file:
    # ToDo: Add the following two columns:
    ##
    csv_header_string = f"\"incident_date\",\"response_unit\",\"call_type\",\"dispatch_time\",\"enroute_time\",\"arrive_time\",\"time_in_service\"\n"
    # create a text file for writing
    # print(f"Original len(temp_data_frame_w_dates) = {length}")
    outputfilelength = len(emergency_data_list)
    # print(f"emergency_data_list content is {outputfilelength} in length")
    with open(csv_data_filename, "a+") as f:
        f.writelines(csv_header_string)
        f.writelines(emergency_data_list)

        """
        for key in temp_dict:
            print(f'{type(key)}')
        counter += 1
        """
    # print(f'{emergency_data.head()}')
    """
    target_file = 'headers.py'
    try:
        fprUtil = shutil.which(target_file)
    except shutil.Error as err:
        raise Exception(f'{err}')
    if fprUtil is None:
        print(f'Did not find {target_file} in the path. Returned: {fprUtil}')
    else:
        print(f'Found: {fprUtil}')
    """
    # print(f"len(temp_data_frame_w_dates) = {length}")

    print(f"{report_end(str(csv_data_filename))}")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
