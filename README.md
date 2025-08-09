# Emergency Call Data SQL Database  

Consolidate some of the Lincoln County emergency service response data into a simple database. 


### Starting with the "clean," munged data, transfer it into an SQL database  
Because it is available virtually everywhere with a minimum of fuss, I used [SQLite](https://sqlite.org/).  


#### Assembled for quick aggregation of Lincoln County, Nebraska Emergency Service Response Data  

The "clean," munged data has the layout below:  

```python
table_name = 'emergency_calls'

create_table_with_types = '''CREATE TABLE IF NOT EXISTS emergency_calls( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_date TEXT NOT NULL,
    incident_date_year_only INTEGER NOT NULL,
    incident_num INTEGER NOT NULL,
    response_unit TEXT NOT NULL,
    response_level TEXT NOT NULL,
    call_type TEXT NOT NULL,
    sub_category TEXT NOT NULL,
    determinant_description TEXT NOT NULL,
    dispatch_time TEXT NOT NULL,
    dispatch_time_in_seconds INTEGER NOT NULL,
    enroute_time TEXT NOT NULL,
    enroute_time_in_seconds INTEGER NOT NULL,
    arrive_time TEXT NOT NULL,
    arrive_time_in_seconds INTEGER NOT NULL,
    response_time_in_seconds INTEGER NOT NULL,
    response_time TEXT NOT NULL,
    time_in_service TEXT NOT NULL,
    time_in_service_in_seconds INTEGER NOT NULL);
    '''

```

And the input data looks like:  

```csv
incident_date,incident_date_year_only,incident_num,response_unit,response_level,call_type,sub_category,determinant_description,dispatch_time,dispatch_time_in_seconds,enroute_time,enroute_time_in_seconds,arrive_time,arrive_time_in_seconds,response_time,response_time_in_seconds,time_in_service,time_in_service_in_seconds
2010-01-01,2010,10000031,WAVE12,MA,33C2,CTNIMRS,CTNIMRS,06:51:33,24693,07:03:23,25403,07:06:23,25583,00:14:50,890,01:26:48,5208
2010-01-01,2010,10000034,WAVE11,MA,28C4,CTNIMRS,CTNIMRS,08:05:59,29159,08:06:00,29160,08:08:21,29301,00:02:22,142,00:59:47,3587
2010-01-01,2010,10000043,MWM31,PR,17A1,alpha,marked (*) not dangerous body area with deformity,09:51:58,35518,10:04:41,36281,10:18:57,37137,00:26:59,1619,02:08:33,7713
2010-01-01,2010,10000043,PLEA1,PR,17A1,alpha,marked (*) not dangerous body area with deformity,09:51:58,35518,09:57:20,35840,09:59:24,35964,00:07:26,446,00:40:12,2412
2010-01-01,2010,10000056,SE1,OM,19D1,delta,not alert,15:48:32,56912,15:48:53,56933,15:53:29,57209,00:04:57,297,00:20:35,1235
2010-01-01,2010,10000056,SE12,OM,19D1,delta,not alert,15:58:26,57506,15:53:39,57219,15:58:29,57509,00:00:03,3,00:33:07,1987
2010-01-02,2010,10000088,8707,FE,FIREC,charlie,"1 bat, 3 engine, 2 truck, air14, 1 medic, duty insp, ems 1",02:02:55,7375,02:02:59,7379,02:59:41,10781,00:56:46,3406,02:48:52,10132
2010-01-02,2010,10000088,CERE1,FE,FIREC,charlie,"1 bat, 3 engine, 2 truck, air14, 1 medic, duty insp, ems 1",01:41:51,6111,01:45:11,6311,01:51:58,6718,00:10:07,607,02:58:42,10722
2010-01-02,2010,10000088,RAYM1,FE,FIREC,charlie,"1 bat, 3 engine, 2 truck, air14, 1 medic, duty insp, ems 1",01:46:16,6376,01:50:42,6642,02:07:09,7629,00:20:53,1253,01:52:36,6756
```

This was assembled to consolidate some of the Lincoln County, Nebraska emergency service response data into an SQL database to make it easier for others to explore.  

Two tools for exploring the SQLite-hosted data:  
https://sqlitebrowser.org  
or in your browser:  
https://inloop.github.io/sqlite-viewer/  
(*When I was required to use databases from a range of vendors, I also used https://www.heidisql.com/ and it supports SQLite as well.*)  



## The databases  

In this use case the input data is in a csv file [2025-08-01_emerg_data_organized_step_four.csv].  The output is in SQLite .db files.  
How did I get there?  Here were the steps:



### STEP ONE:  

(All of this work was performed using Python 3.11)

In this use case the input data is in a csv file [2025-08-01_emerg_data_organized_step_four.csv].  The output is in SQLite .db files.  
How did I get there?  Here were the steps:

* [step_one_main.py](https://github.com/mccright/emerg-call-data-review/blob/main/step_one_main.py) is used to convert the original data from Lincoln County into a dataset rationalized for this exercise -- it output [2024-12-11_emerg_data_organized.csv](2024-12-11_emerg_data_organized.csv).  

When you run it, be patient. It is slow. To show you it is really doing work it will emit the number of record that it is processing from the original data file and then a short end-of-processing report like that below:  
```terminal
C:\dev\pycharm\emerg-call-data-timeseries\venv\Scripts\python.exe C:\dev\pycharm\emerg-call-data-timeseries\step_one_main.py 

- - - - - - - - - - - - - - - - - - - - - - - -
C:\dev\pycharm\emerg-call-data-timeseries\step_one_main.py
Report started at: 2025-07-31 21:55:25.606683 local, 2025-08-01 02:55:25.606683+00:00 UTC
Root of target filesystem: C:\dev\pycharm\emerg-call-data-timeseries
- - - - - - - - - - - - - - - - - - - - - - - -
Record: 1
Record: 2

...
Record: 19518
Record: 19519

- - - - - - - - - - - - - - - - - - - - - - - -
C:\dev\pycharm\emerg-call-data-timeseries\step_one_main.py
Report started at: 2025-07-31 21:55:25.606683 local, 2025-08-01 02:55:25.606683+00:00 UTC
Report ended at: 2025-07-31 23:25:53.041389 local, 2025-08-01 04:25:53.041389+00:00 UTC
Report took: 1:30:27.434706
Reporting processed 19520 input records and output 22829 records
Report Output Files: C:\dev\pycharm\emerg-call-data-timeseries\2025-07-31_emerg_data_organized_step_one.csv
- - - - - - - - - - - - - - - - - - - - - - - -

Process finished with exit code 0
```


### STEP TWO:  

* [step_two_optimize_data_se.py](https://github.com/mccright/emerg-call-data-review/blob/main/step_two_optimize_data_se.py) ingests the organized data from [step_one_main.py](https://github.com/mccright/emerg-call-data-review/blob/main/step_one_main.py) above, and adds columns for the year of each record, and for each column that contains a ```time``` value, it converts the value into a ```seconds``` value to make it easier to do math and comparisons with the original *times*.  

It runs faster than the [main_step_one.py](https://github.com/mccright/emerg-call-data-review/blob/main/main_step_one.py) and ends with a short end-of-processing report like that below:  

```terminal
C:\dev\pycharm\emerg-call-data-timeseries\venv\Scripts\python.exe C:\dev\pycharm\emerg-call-data-timeseries\step_two_optimize_data_se.py 


- - - - - - - - - - - - - - - - - - - - - - - -
C:\dev\pycharm\emerg-call-data-timeseries\step_two_optimize_data_se.py
Report started at: 2025-08-01 06:38:16.764383 local, 2025-08-01 11:38:16.764383+00:00 UTC
Root of target filesystem: C:\dev\pycharm\emerg-call-data-timeseries
- - - - - - - - - - - - - - - - - - - - - - - -
There are 22829 records and 10 columns in 2025-07-31_emerg_data_organized_step_one.csv


- - - - - - - - - - - - - - - - - - - - - - - -
C:\dev\pycharm\emerg-call-data-timeseries\step_two_optimize_data_se.py
Report started at: 2025-08-01 06:38:16.764383 local, 2025-08-01 11:38:16.764383+00:00 UTC
Report ended at: 2025-08-01 06:38:18.728840 local, 2025-08-01 11:38:18.728840+00:00 UTC
Report took: 0:00:01.964457
Reporting processed 22829 input records and output 22829 records
Report Output Files: C:\dev\pycharm\emerg-call-data-timeseries\2025-08-01_emerg_data_date_to_year_add_time_in_seconds_columns_step_two.csv
- - - - - - - - - - - - - - - - - - - - - - - -

Process finished with exit code 0
```


### STEP THREE:  

```terminal
C:\dev\pycharm\emerg-call-data-timeseries\venv\Scripts\python.exe C:\dev\pycharm\emerg-call-data-timeseries\step_three_add_response_time_columns.py 
22829 rows in the whole dataframe
84 rows in filtered response_units
time_to_arrival_list is type: <class 'list'>
-----------------------------------------

Process finished with exit code 0
```


### STEP FOUR:  

* Now calculate the response times and insert columns to document them in seconds and human-freindly hh:mm:ss formats.  Use: [step_four_build_criticality_columns.py](https://github.com/mccright/emerg-call-data-review/blob/main/step_four_build_criticality_columns.py)
It runs in seconds, not minutes...  

```terminal
C:\Files\dev\github\emerg-call-data-timeseries-temp\venv\Scripts\python.exe C:\Files\dev\pycharm\emerg-call-data-timeseries-temp\step_four_build_criticality_columns.py 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
The number of columns in "2025-08-01_add_response_time_columns_step_three.csv" is: 16
csv_raw_data type = <class 'csv.DictReader'>
 input header fields/columns: ['incident_date', 'incident_date_year_only', 'incident_num', 'response_unit', 'response_level', 'call_type', 'dispatch_time', 'dispatch_time_in_seconds', 'enroute_time', 'enroute_time_in_seconds', 'arrive_time', 'arrive_time_in_seconds', 'response_time_in_seconds', 'response_time', 'time_in_service', 'time_in_service_in_seconds']
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
21991 found
838 missing
CTNIMRS == Call Type not in Master Run Sheet.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
The number of columns in "C:\Files\dev\pycharm\emerg-call-data-timeseries-temp\2025-08-02_emerg_data_organized_step_four.csv" is: 18
output header fields/columns: ['incident_date', 'incident_date_year_only', 'incident_num', 'response_unit', 'response_level', 'call_type', 'sub_category', 'determinant_description', 'dispatch_time', 'dispatch_time_in_seconds', 'enroute_time', 'enroute_time_in_seconds', 'arrive_time', 'arrive_time_in_seconds', 'response_time', 'response_time_in_seconds', 'time_in_service', 'time_in_service_in_seconds']
Data processing complete. 
Input file is "2025-08-01_add_response_time_columns_step_three.csv".
Result saved in "C:\Files\dev\pycharm\emerg-call-data-timeseries-temp\2025-08-02_emerg_data_organized_step_four.csv".

Process finished with exit code 0

```



### STEP 5:  

Then use one of the scripts below to create a database.  
* [step_five_csv-to-sqlite_using-sqlite3.py](step_five_csv-to-sqlite_using-sqlite3.py) is used to create [2025-08-01_emerg_data_organized_via_sqlite3.db].  

* [csv-to-sqlite_using-sqlalchemy.py](csv-to-sqlite_using-sqlalchemy.py) is used to create [2024-12-11_emerg_data_organized_via_sqlalchemy.db].  

```terminal
C:\dev\pycharm\emerg-call-data-timeseries\venv\Scripts\python.exe C:\dev\pycharm\emerg-call-data-timeseries\step_five_csv-to-sqlite_using-sqlite3.py 
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 22829 entries, 0 to 22828
Data columns (total 18 columns):
 #   Column                      Non-Null Count  Dtype 
---  ------                      --------------  ----- 
 0   incident_date               22829 non-null  object
 1   incident_date_year_only     22829 non-null  int64 
 2   incident_num                22829 non-null  int64 
 3   response_unit               22829 non-null  object
 4   response_level              22827 non-null  object
 5   call_type                   22829 non-null  object
 6   sub_category                22799 non-null  object
 7   determinant_description     22817 non-null  object
 8   dispatch_time               22829 non-null  object
 9   dispatch_time_in_seconds    22829 non-null  int64 
 10  enroute_time                22829 non-null  object
 11  enroute_time_in_seconds     22829 non-null  int64 
 12  arrive_time                 22829 non-null  object
 13  arrive_time_in_seconds      22829 non-null  int64 
 14  response_time               22829 non-null  object
 15  response_time_in_seconds    22829 non-null  int64 
 16  time_in_service             22829 non-null  object
 17  time_in_service_in_seconds  22829 non-null  int64 
dtypes: int64(7), object(11)
memory usage: 3.1+ MB

Process finished with exit code 0
```


### Exploring the data...  

See the [Explore_the_data-w-SQL.md](Explore_the_data-w-SQL.md) page for a range of SQL for exploring the data.  

