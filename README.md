# Emergency Call Data SQL Database  

Consolidate some of the Lincoln County emergency service response data into a simple database. 


### Starting with the "clean," munged data, transfer it into an SQL database  
Because it is available virtually everywhere with a minimum of fuss, I used [SQLite](https://sqlite.org/).  


#### Assembled for quick aggregation of Lincoln County, Nebraska Emergency Service Response Data  

The "clean," munged data has the layout below:  

```csv
"incident_date","incident_date_year_only","response_unit","call_type","dispatch_time","dispatch_time_in_seconds","enroute_time","enroute_time_in_seconds","arrive_time","arrive_time_in_seconds","time_in_service","time_in_service_in_seconds"
"2010-01-01","2010","WAVE12","33C2","06:51:33","24693","07:03:23","25403","07:06:23","25583","01:26:48","5208"
"2010-01-01","2010","WAVE11","28C4","08:05:59","29159","08:06:00","29160","08:08:21","29301","00:59:47","3587"

```

This was assembled to consolidate some of the Lincoln County, Nebraska emergency service response data into an SQL database to make it easier for others to explore.  

Two tools for exploring the SQLite-hosted data:  
https://sqlitebrowser.org  
or in your browser:  
https://inloop.github.io/sqlite-viewer/  


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

* [csv-to-sqlite_using-sqlite3.py](csv-to-sqlite_using-sqlite3.py) is used to create [2025-02-13_emerg_data_organized_via_sqlite3.db].  

* [csv-to-sqlite_using-sqlalchemy.py](csv-to-sqlite_using-sqlalchemy.py) is used to create [2024-12-11_emerg_data_organized_via_sqlalchemy.db].  


### My working notes...  

Normally response_unit is the name of a given team, dispatch_time is when they received a call for service and time_in_service is the amount of time a given response_unit spent on that given service.  

LFR Ambulances are noted by "M," signifying "Medic" followed by a number.  
	These include:  
		'''M1, M2, M3, M5, M6, M7, M8, M10, M21, M24, M25'''  
		There may be other M-units listed in the data, but my sense is that those are typos or are very rarely called and will not affect the general sense of the data.  

First, review the data for response_unit values that begin with 'M':  
```terminal
SELECT response_unit, count(DISTINCT call_type) distinct_call_types, count(response_unit) total_call_count
   FROM emergency_calls
   WHERE response_unit LIKE 'M%'
   GROUP BY response_unit
   ORDER BY distinct_call_types;

response_unit	distinct_call_types	total_call_count
M21	1	1
MILF10	1	1
MWM33	1	1
MWM35	2	2
MWM34	4	4
M214	6	7
MWM32	6	6
M1	7	13
M211	9	9
M24	9	10
M25	10	15
MALC2	13	25
M10	33	61
MWM31	39	56
M2	113	307
M7	132	367
M3	155	609
M8	155	550
MALC10	179	543
M5	202	984
MALC1	234	1213
M6	309	2128

```

There are 11 response units that have a total_call_count of less than 25, so lets drop them and query only the remaining response_unit names:
* Quality check for those "M" LFR ambulance designators in the data tht have more than 24 calls:  
```terminal
SELECT response_unit, count(DISTINCT call_type) distinct_call_types, count(response_unit) total_call_count
   FROM emergency_calls
   WHERE response_unit IN ('M6', 'MALC1', 'M5', 'M3', 'M8', 'MALC10', 'M7', 'M2', 'M10', 'MWM31', 'MALC2')
   GROUP BY response_unit
   ORDER BY distinct_call_types;

response_unit	distinct_call_types	total_call_count
MALC2	13	25
M10	33	61
MWM31	39	56
M2	113	307
M7	132	367
M3	155	609
M8	155	550
MALC10	179	543
M5	202	984
MALC1	234	1213
M6	309	2128

```


What is the median response time on major calls for County ambulances each year?  
"Major Calls" are "call_type":  
		 That include "Sub Category" C (Charlie), D (Delta), or E (Echo) \  
		 as defined by the file "110520 Master Run Sheet.xlsx"  
		call_type:  
			FIREC, GRASFIRE, RSALARM, ECHO, CARFIRE, MEDC, MEDD, MEDE  

```SQL
SELECT response_unit, count(response_unit) total_call_count, AVG(time_in_service_in_seconds) avg_time_in_service_in_seconds
   FROM emergency_calls
   WHERE call_type IN ('FIREC', 'GRASFIRE', 'RSALARM', 'ECHO', 'CARFIRE', 'MEDC', 'MEDD', 'MEDE')
   GROUP BY response_unit
   ORDER BY time_in_service_in_seconds;
```
Returns 101 rows.  

Sanity check these values by just listing all the `time_in_service` values for each response_unit:  
```SQL
SELECT response_unit, count(response_unit) total_call_count, GROUP_CONCAT(time_in_service_in_seconds) list_of_times_in_service_in_seconds
   FROM emergency_calls
   WHERE call_type IN ('FIREC', 'GRASFIRE', 'RSALARM', 'ECHO', 'CARFIRE', 'MEDC', 'MEDD', 'MEDE')
   GROUP BY response_unit
   ORDER BY total_call_count;
```


### Reference thoughts -- unfinished  

Table Definition (https://sqlite.org/datatype3.html)  
Datatypes In SQLite databases are "Storage Classes":  
   NULL, INTEGER, REAL, TEXT and BLOB  
[REAL: only the first 15 significant decimal digits of the number are preserved]  
and columns have "type affinity":  
   TEXT, NUMERIC, INTEGER, REAL and BLOB  
A TEXT DateTime is stored as ISO8601 strings ("YYYY-MM-DD HH:MM:SS.SSS").  
   See: https://sqlite.org/lang_datefunc.html to use them.  


how to create a date field in an sqlite database  
https://duckduckgo.com/?t=h_&q=how+to+create+a+date+field+in+an+sqlite+database&ia=web  

https://sqlite.org/pragma.html#pragma_index_info  
Built-in Aggregate Functions  
https://www.sqlite.org/lang_aggfunc.html  

```terminal
PRAGMA table_list;
PRAGMA table_list(emergency_calls);
PRAGMA main.table_info(emergency_calls);
PRAGMA main.table_xinfo(emergency_calls);
PRAGMA main.index_list(emergency_calls);

SELECT COUNT(*) FROM emergency_calls
SELECT * FROM 'emergency_calls' LIMIT 0,200
SELECT * FROM 'emergency_calls' WHERE incident_date < "2010-01-02" LIMIT 0,200
SELECT * FROM 'emergency_calls' WHERE incident_date < "2010-01-02" OR incident_date > "2010-01-02" LIMIT 0,60
SELECT * FROM 'emergency_calls' WHERE dispatch_time < "09:51:59" LIMIT 0,200

# The following emits the number of calls (any call_type) per unit over the entire db scope
# ordered by response_unit
SELECT response_unit, count(call_type)
   FROM emergency_calls
   GROUP BY response_unit
#
# The following emits the number of distinct call_types per unit over the entire db scope
# ordered by call_type_count
SELECT response_unit, count(DISTINCT call_type) call_type_count
   FROM emergency_calls
   GROUP BY response_unit
   ORDER BY call_type_count;
#
# The following emits the number of distinct_call_types, total_call_count (any call_type) per unit over the entire db scope
# This may help identify (then weed out) some noise in the data.
# For example, should be "care about" a response_unit that has one call over 10 years? ...2? ...4? 
# What is the threshold below which we ignore given response_unit's records?
SELECT response_unit, count(DISTINCT call_type) distinct_call_types, count(response_unit) total_call_count
   FROM emergency_calls
   GROUP BY response_unit
   ORDER BY distinct_call_types;
#
# The following emits the number of distinct_call_types, total_call_count (any call_type) per unit over the entire db scope
# ordered by the response_unit name.  This may be easier for some to navigate.  The question remains, 
# What is the # of calls threshold below which we ignore given response_unit's records?
# This may help identify (then weed out) some noise in the data.
SELECT response_unit, count(DISTINCT call_type) distinct_call_types, count(response_unit) total_call_count
   FROM emergency_calls
   GROUP BY response_unit
   ORDER BY response_unit;
#
# The following emits each unit and a list of all the call_types in their records
SELECT response_unit, GROUP_CONCAT(call_type) call_types
   FROM emergency_calls
   GROUP BY response_unit
   HAVING MIN(call_type) <> MAX(call_type);
#
# What call types are the longest for teams?
SELECT response_unit, time_in_service
   FROM emergency_calls
   WHERE time_in_service > "01:30:00"
   GROUP BY call_type
#
# What call types are the longest, and how long is each call of that type?
SELECT call_type, GROUP_CONCAT(time_in_service)
    FROM emergency_calls
    WHERE time_in_service > "01:45:00"
    GROUP BY call_type
    ORDER BY call_type
#
# What call types do each of the units serve?
SELECT call_type, GROUP_CONCAT(response_unit)
    FROM emergency_calls
    GROUP BY call_type
    ORDER BY call_type
#
# The following emits each unit and a list of all the call_types in their records by date
# This illustrates which units are dealing with more calls per day
SELECT response_unit, count(call_type)
   FROM emergency_calls
   GROUP BY response_unit
# or 
SELECT incident_date, response_unit, GROUP_CONCAT(call_type) call_types
   FROM emergency_calls
   GROUP BY response_unit

# incident_date","response_unit","call_type","dispatch_time","enroute_time","arrive_time","time_in_service"
```


