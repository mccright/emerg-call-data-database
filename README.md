# Emergency Call Data SQL Database  

Consolidate some of the Lincoln County emergency service response data into a simple database. 


### Starting with the "clean," munged data, transfer it into an SQL database  
Because it is available virtually everywhere with a minimum of fuss, I used [SQLite](https://sqlite.org/).  


#### Assembled for quick aggregation of Lincoln County, Nebraska Emergency Service Response Data  

The "clean," munged data has the layout below:  

```csv
incident_date,incident_date_year_only,response_unit,call_type,dispatch_time,dispatch_time_in_seconds,enroute_time,enroute_time_in_seconds,arrive_time,arrive_time_in_seconds,response_time_in_seconds,response_time,time_in_service,time_in_service_in_seconds
2010-01-01,2010,WAVE12,33C2,06:51:33,24693,07:03:23,25403,07:06:23,25583,890,00:14:50,01:26:48,5208
2010-01-01,2010,WAVE11,28C4,08:05:59,29159,08:06:00,29160,08:08:21,29301,142,00:02:22,00:59:47,3587
2010-01-01,2010,MWM31,17A1,09:51:58,35518,10:04:41,36281,10:18:57,37137,1619,00:26:59,02:08:33,7713

```

This was assembled to consolidate some of the Lincoln County, Nebraska emergency service response data into an SQL database to make it easier for others to explore.  

Two tools for exploring the SQLite-hosted data:  
https://sqlitebrowser.org  
or in your browser:  
https://inloop.github.io/sqlite-viewer/  
(*When I was required to use databases from a range of vendors, I also used https://www.heidisql.com/ and it supports SQLite as well.*)  



## The databases  

In this use case the input data is in a csv file [2024-12-11_emerg_data_organized.csv].  The output is in SQLite .db files.  

* [main_step_one.py](https://github.com/mccright/emerg-call-data-review/blob/main/main_step_one.py) is used to convert the original data from Lincoln County into a dataset rationalized for this exercise -- it output [2024-12-11_emerg_data_organized.csv](2024-12-11_emerg_data_organized.csv).  

When you run it, be patient. It is slow. To show you it is really doing work it will emit the number of record that it is processing from the original data file and then a short end-of-processing report like that below:  
```terminal
- - - - - - - - - - - - - - - - - - - - - - - -
C:\Files\dev\pycharm\emerg-call-data-timeseries-temp\main.py
Report started at: 2025-02-13 22:01:30.764194 local, 2025-02-14 04:01:30.764194+00:00 UTC
Report ended at: 2025-02-13 22:50:03.953248 local, 2025-02-14 04:50:03.953248+00:00 UTC
Report took: 0:48:33.189054
Reporting processed 19520 input records and output 22829 records
Report Output Files: C:\Files\dev\pycharm\emerg-call-data-timeseries-temp\2025-02-13_emerg_data_organized_step_one.csv
- - - - - - - - - - - - - - - - - - - - - - - -


Process finished with exit code 0
```

* [optimize_data_set_step_two.py](https://github.com/mccright/emerg-call-data-review/blob/main/optimize_data_set_step_two.py) ingests the organized data from [main_step_one.py](https://github.com/mccright/emerg-call-data-review/blob/main/main_step_one.py) above, and adds columns for the year of each record, and for each column that contains a ```time``` value, it converts the value into a ```seconds``` value to make it easier to do math and comparisons with the original *times*.  

It runs faster than the [main_step_one.py](https://github.com/mccright/emerg-call-data-review/blob/main/main_step_one.py) and ends with a short end-of-processing report like that below:  
```terminal
- - - - - - - - - - - - - - - - - - - - - - - -
C:\Files\dev\pycharm\emerg-call-data-timeseries-temp\optimize_data_set.py
Report started at: 2025-02-14 07:34:28.073455 local, 2025-02-14 13:34:28.073455+00:00 UTC
Report ended at: 2025-02-14 07:34:29.766743 local, 2025-02-14 13:34:29.766743+00:00 UTC
Report took: 0:00:01.693288
Reporting processed 22829 input records and output 22829 records
Report Output Files: C:\Files\dev\pycharm\emerg-call-data-timeseries-temp\2025-02-14_emerg_data_date_is_now_year_new_time_in_seconds_columns_optimized.csv
- - - - - - - - - - - - - - - - - - - - - - - -

Process finished with exit code 0
```

* Now calculate the response times and insert columns to document them in seconds and human-freindly hh:mm:ss formats.  Use: [add_response_time_columns_step_three.py](https://github.com/mccright/emerg-call-data-review/blob/main/add_response_time_columns_step_three.py)
It runs in seconds, not minutes...  

It outputs the data in the following format:
```terminal
RangeIndex: 22829 entries, 0 to 22828
Data columns (total 14 columns):
 #   Column                      Non-Null Count  Dtype 
---  ------                      --------------  ----- 
 0   incident_date               22829 non-null  object
 1   incident_date_year_only     22829 non-null  int64 
 2   response_unit               22829 non-null  object
 3   call_type                   22829 non-null  object
 4   dispatch_time               22829 non-null  object
 5   dispatch_time_in_seconds    22829 non-null  int64 
 6   enroute_time                22829 non-null  object
 7   enroute_time_in_seconds     22829 non-null  int64 
 8   arrive_time                 22829 non-null  object
 9   arrive_time_in_seconds      22829 non-null  int64 
 10  response_time_in_seconds    22829 non-null  int64 
 11  response_time               22829 non-null  object
 12  time_in_service             22829 non-null  object
 13  time_in_service_in_seconds  22829 non-null  int64 
dtypes: int64(6), object(8)
```

Then use one of the scripts below to create a database.  
* [csv-to-sqlite_using-sqlite3.py](csv-to-sqlite_using-sqlite3.py) is used to create [2025-02-13_emerg_data_organized_via_sqlite3.db].  

* [csv-to-sqlite_using-sqlalchemy.py](csv-to-sqlite_using-sqlalchemy.py) is used to create [2024-12-11_emerg_data_organized_via_sqlalchemy.db].  


### Exploring the data...  

See the [Explore_the_data-w-SQL.md](Explore_the_data-w-SQL.md) page for a range of SQL for exploring the data.  

