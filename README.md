# Emergency Call Data SQL Database  

Consolidate some of the Lincoln County emergency service response data into a simple database. 

# Emergency Call Data SQL Database  

## Starting with the "clean," munged data, transfer it into an SQL database  
Because it is available virtually everywhere with a minimum of fuss, I used [SQLite](https://sqlite.org/).  


## Assembled for quick aggregation of Lincoln County, Nebraska Emergency Service Response Data  

The "clean," munged data has the layout below:  

```csv
"incident_date","response_unit","call_type","dispatch_time","enroute_time","arrive_time","time_in_service"
"2010-01-01","WAVE12","33C2","06:51:33","07:03:23","07:06:23","01:26:48"
"2010-01-01","WAVE11","28C4","08:05:59","08:06:00","08:08:21","00:59:47"
"2010-01-01","MWM31","17A1","09:51:58","10:04:41","10:18:57","02:08:33"
"2010-01-01","PLEA1","17A1","09:51:58","09:57:20","09:59:24","00:40:12"
"2010-01-01","SE1","19D1","15:48:32","15:48:53","15:53:29","00:20:35"
"2010-01-01","SE12","19D1","15:58:26","15:53:39","15:58:29","00:33:07"
"2010-01-02","8707","FIREC","02:02:55","02:02:59","02:59:41","02:48:52"
"2010-01-02","CERE1","FIREC","01:41:51","01:45:11","01:51:58","02:58:42"
"2010-01-02","RAYM1","FIREC","01:46:16","01:50:42","02:07:09","01:52:36"
"2010-01-02","WAVE1","FIREC","01:46:16","01:50:45","02:19:25","01:07:18"
"2010-01-02","SW1","FIREB","16:33:09","16:34:21","16:49:30","00:26:58"
"2010-01-02","M5","29D2P","19:08:35","19:09:19","19:21:31","00:13:36"
"2010-01-02","WAVE12","29D2P","19:08:35","19:12:54","19:21:36","00:13:42"
"2010-01-02","SE1","10C4","22:55:30","22:56:21","23:09:01","00:48:29"
"2010-01-02","SE11","10C4","22:55:30","22:57:33","23:08:39","00:48:27"
"2010-01-03","VALP1","FIREA","08:17:59","08:23:35","08:30:10","00:35:54"

```

This was assembled to consolidate some of the Lincoln County, Nebraska emergency service response data into an SQL database to make it easier for others to explore.  

Two tools for exploring the SQLite-hosted data:  
https://sqlitebrowser.org  
or in your browser:  
https://inloop.github.io/sqlite-viewer/  


## The databases  

In this use case the input data is in a csv file [2024-12-11_emerg_data_organized.csv].  The output is in SQLite .db files.  

* [main.py](main.py) is used to convert the original data from Lincoln County into a dataset rationalized for this exercise -- it output [2024-12-11_emerg_data_organized.csv].

* [csv-to-sqlite_using-sqlite3.py](csv-to-sqlite_using-sqlite3.py) is used to create [2024-12-11_emerg_data_organized_via_sqlite3.db].    

* [csv-to-sqlite_using-sqlalchemy.py](csv-to-sqlite_using-sqlalchemy.py) is used to create [2024-12-11_emerg_data_organized_via_sqlalchemy.db].  


## My working notes...  

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
SELECT response_unit, count(response_unit) total_call_count, AVG(time_in_service) avg_time_in_service
   FROM emergency_calls
   WHERE call_type IN ('FIREC', 'GRASFIRE', 'RSALARM', 'ECHO', 'CARFIRE', 'MEDC', 'MEDD', 'MEDE')
   GROUP BY response_unit
   ORDER BY avg_time_in_service;
```
Returns 101 rows.  

Sanity check these values by just listing all the `time_in_service` values for each response_unit:  
```SQL
SELECT response_unit, count(response_unit) total_call_count, GROUP_CONCAT(time_in_service) times_in_service
   FROM emergency_calls
   WHERE call_type IN ('FIREC', 'GRASFIRE', 'RSALARM', 'ECHO', 'CARFIRE', 'MEDC', 'MEDD', 'MEDE')
   GROUP BY response_unit
   ORDER BY total_call_count;
```


## Reference thoughts -- unfinished  

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


