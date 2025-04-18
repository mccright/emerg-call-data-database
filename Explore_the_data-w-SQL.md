# Emergency Call Data SQL Database  

Consolidated Lincoln County, Nebraska emergency service response data in an SQL database to make it easier for others to explore.  

Two tools for exploring the SQLite-hosted data:  
https://sqlitebrowser.org  
or in your browser:  
https://inloop.github.io/sqlite-viewer/  


## The databases  

* [csv-to-sqlite_using-sqlite3.py](csv-to-sqlite_using-sqlite3.py) is used to create [2025-02-13_emerg_data_organized_via_sqlite3.db](2025-02-13_emerg_data_organized_via_sqlite3.db).  

### Database Schema  
You will need to know the column names & types to craft your SQL.  
```sql
create_table_with_types = '''CREATE TABLE IF NOT EXISTS emergency_calls( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_date TEXT NOT NULL,
    incident_date_year_only INTEGER NOT NULL,
    response_unit TEXT NOT NULL,
    call_type TEXT NOT NULL,
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


My primary tool for exploring the SQLite-hosted data is: https://sqlitebrowser.org  
When I was required to use databases from a range of vendors, I also used https://www.heidisql.com/.  


### My working notes...  

What period of time does this data represent?  In this case, we can count the unique *years* listed in all the database records.  
```SQL
SELECT count(DISTINCT incident_date_year_only) AS incident_date_year_count
   FROM 'emergency_calls'
```
Result = 11  


The ```response_unit``` is the name of a given team.  How many unique ```response_unit``` strings are included in the database?  
```SQL
SELECT count(DISTINCT response_unit) AS response_unit_count
   FROM 'emergency_calls'
```
Result = 135  
This number is inflated because the initial responder to an incident call is (*at least most of the time*) an individual, who is a member of the ```response_unit``` that *may* end up responding to a given call.  



The ```call_type``` is an assembledge of indicators that coarsely describe the nature and priority of the situation that is associated with any given incident. How many unique ```call_type``` strings are included in the database?  
```SQL
SELECT count(DISTINCT call_type) AS call_type_count
   FROM 'emergency_calls'
```
Result = 556  

The response_unit is the name of a given team, dispatch_time is when they received a call for service and time_in_service is the amount of time a given response_unit spent on that given service call.  

```terminal
LFR Ambulances are noted by "M," signifying "Medic" followed by a number.  
	These include:  
		'''M1, M2, M3, M5, M6, M7, M8, M10, M21, M24, M25'''  
		There may be other M-units listed in the data, but my sense is that those are typos or are very rarely called and will not affect the general sense of the data.
```

First, review the data for response_unit values that begin with 'M':  
```SQL
SELECT response_unit, count(DISTINCT call_type) distinct_call_types, count(response_unit) total_call_count
   FROM emergency_calls
   WHERE response_unit LIKE 'M%'
   GROUP BY response_unit
   ORDER BY distinct_call_types;
```
```terminal
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
```SQL
SELECT response_unit, count(DISTINCT call_type) AS distinct_call_types, count(response_unit) AS total_call_count
   FROM emergency_calls
   WHERE response_unit IN ('M6', 'MALC1', 'M5', 'M3', 'M8', 'MALC10', 'M7', 'M2', 'M10', 'MWM31', 'MALC2')
   GROUP BY response_unit
   ORDER BY distinct_call_types;
```
```terminal
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
```terminal
"Major Calls" are "call_type":  
		 That include "Sub Category" C (Charlie), D (Delta), or E (Echo) \  
		 as defined by the file "[110520 Master Run Sheet.xlsx](https://github.com/mccright/emerg-call-data-review/blob/main/rawdata/110520_Master_Run_Sheet.xlsx)"  
		call_type:  
			FIREC, GRASFIRE, RSALARM, ECHO, CARFIRE, MEDC, MEDD, MEDE
```

```SQL
SELECT response_unit, count(response_unit) AS total_call_count, AVG(time_in_service_in_seconds) AS avg_time_in_service_in_seconds
   FROM emergency_calls
   WHERE call_type IN ('FIREC', 'GRASFIRE', 'RSALARM', 'ECHO', 'CARFIRE', 'MEDC', 'MEDD', 'MEDE')
   GROUP BY response_unit
   ORDER BY time_in_service_in_seconds;
```
Returns 101 rows.  

Sanity check these values by just listing all the `time_in_service` values for each response_unit and reviewing them visually to confirm your assumptions:  
```SQL
SELECT response_unit, count(response_unit) AS total_call_count, GROUP_CONCAT(time_in_service_in_seconds) AS list_of_times_in_service_in_seconds
   FROM emergency_calls
   WHERE call_type IN ('FIREC', 'GRASFIRE', 'RSALARM', 'ECHO', 'CARFIRE', 'MEDC', 'MEDD', 'MEDE')
   GROUP BY response_unit
   ORDER BY total_call_count;
```


```SQL
-- example of building a query for a specified list of values
SELECT response_unit, count(DISTINCT call_type) AS distinct_call_types, count(response_unit) AS total_call_count
   FROM emergency_calls
   WHERE response_unit IN ('M6', 'MALC1', 'M5', 'M3', 'M8', 'MALC10', 'M7', 'M2', 'M10', 'MWM31', 'MALC2')
   GROUP BY response_unit
   ORDER BY distinct_call_types;
```


```SQL
-- example of using 'LIKE' when you don't want to build a list
SELECT response_unit, count(DISTINCT call_type) distinct_call_types, count(response_unit) total_call_count
   FROM emergency_calls
   WHERE response_unit LIKE 'M%'
   GROUP BY response_unit
   ORDER BY distinct_call_types;
```


```SQL
SELECT response_unit, count(response_unit) AS total_call_count, 
CAST(AVG(time_in_service_in_seconds) AS INTEGER) AS time_in_service_in_seconds_integer
   FROM emergency_calls
   WHERE call_type IN ('FIREC', 'GRASFIRE', 'RSALARM', 'ECHO', 'CARFIRE', 'MEDC', 'MEDD', 'MEDE')
   GROUP BY response_unit
   ORDER BY time_in_service_in_seconds_integer;
```


```SQL
-- Average response_time and total call count for a given list of call_type's
-- for each response_unit across all the data
SELECT response_unit, count(response_unit) AS total_call_count, 
CAST(AVG(response_time_in_seconds) AS INTEGER) AS avg_response_time_in_seconds_integer
   FROM emergency_calls
   WHERE call_type IN ('FIREC', 'GRASFIRE', 'RSALARM', 'ECHO', 'CARFIRE', 'MEDC', 'MEDD', 'MEDE')
   GROUP BY response_unit
   ORDER BY avg_response_time_in_seconds_integer;
```


```SQL
SELECT response_unit, call_type, dispatch_time, arrive_time, response_time_in_seconds, response_time
   FROM emergency_calls
   WHERE response_unit LIKE 'E15%'

```


```SQL
-- List of call_type's for each response_unit across all data
SELECT response_unit, GROUP_CONCAT(call_type) call_types
   FROM emergency_calls
   GROUP BY response_unit
   HAVING MIN(call_type) &lt;&gt; MAX(call_type);
```


```SQL
-- average call times by response_unit for a specified year
SELECT incident_date_year_only, response_unit, count(response_unit) total_call_count, AVG(time_in_service_in_seconds) avg_time_in_service_in_seconds
   FROM 'emergency_calls' 
   WHERE (incident_date_year_only = 2019)
   AND (call_type IN ('FIREC', 'GRASFIRE', 'RSALARM', 'ECHO', 'CARFIRE', 'MEDC', 'MEDD', 'MEDE'))
   GROUP BY response_unit
   ORDER BY avg_time_in_service_in_seconds;
```


```SQL
-- average call times by response_unit for a specified year
SELECT incident_date_year_only, response_unit, count(response_unit) total_call_count,
CAST(AVG(response_time_in_seconds) AS INTEGER) AS avg_response_time_in_seconds_integer,
CAST(AVG(time_in_service_in_seconds) AS INTEGER) AS time_in_service_in_seconds_integer
   FROM 'emergency_calls' 
   WHERE (incident_date_year_only = 2019)
   AND (call_type IN ('FIREC', 'GRASFIRE', 'RSALARM', 'ECHO', 'CARFIRE', 'MEDC', 'MEDD', 'MEDE'))
   AND NOT response_unit = 'E15' -- Assume it's entry was a mistake
   GROUP BY response_unit
   ORDER BY avg_response_time_in_seconds_integer DESC;
```


```SQL
-- average incident response times and in-service times by response_unit for a specified range of years
SELECT incident_date_year_only, response_unit, count(response_unit) total_call_count, 
CAST(AVG(response_time_in_seconds) AS INTEGER) AS avg_response_time_in_seconds_integer, 
CAST(AVG(time_in_service_in_seconds) AS INTEGER) AS time_in_service_in_seconds_integer
   FROM 'emergency_calls' 
   WHERE (incident_date_year_only &gt; 2013 AND incident_date_year_only &lt; 2019)
   AND (call_type IN ('FIREC', 'GRASFIRE', 'RSALARM', 'ECHO', 'CARFIRE', 'MEDC', 'MEDD', 'MEDE'))
   GROUP BY incident_date_year_only, response_unit
   ORDER BY response_unit;
</sql>```


```SQL
-- average incident response times and in-service times by specified response_units for each year in dataset
-- The result of AVG() is always a floating point, even if all inputs are integers.
SELECT incident_date_year_only, response_unit, count(response_unit) total_call_count,
CAST(AVG(response_time_in_seconds) AS INTEGER) AS avg_response_time_in_seconds_integer, 
CAST(AVG(time_in_service_in_seconds) AS INTEGER) AS time_in_service_in_seconds_integer
   FROM 'emergency_calls' 
   WHERE (response_unit IN ('M6', 'MALC1', 'M5', 'M3', 'M8', 'MALC10', 'M7', 'M2', 'M10', 'MWM31', 'MALC2'))
   AND (call_type IN ('FIREC', 'GRASFIRE', 'RSALARM', 'ECHO', 'CARFIRE', 'MEDC', 'MEDD', 'MEDE'))
   GROUP BY incident_date_year_only, response_unit
   ORDER BY response_unit, incident_date_year_only;
```


```SQL
-- average incident response times and in-service times 
-- for specified response_units for all years in the dataset.
-- total_call_count is included to help sanity check avg_time_in_service_in_seconds values.
SELECT incident_date_year_only, response_unit, count(response_unit) total_call_count,
CAST(AVG(response_time_in_seconds) AS INTEGER) AS avg_response_time_in_seconds_integer, 
CAST(AVG(time_in_service_in_seconds) AS INTEGER) AS time_in_service_in_seconds_integer
   FROM 'emergency_calls' 
   WHERE (response_unit IN ('M1', 'M2', 'M3', 'M5', 'M6', 'M7', 'M8', 'M10', 'M21', 'M24', 'M25', 'MALC1', 'MALC10', 'MWM31', 'MALC2'))
   AND (call_type IN ('FIREC', 'GRASFIRE', 'RSALARM', 'ECHO', 'CARFIRE', 'MEDC', 'MEDD', 'MEDE'))
   GROUP BY incident_date_year_only, response_unit
   ORDER BY response_unit, incident_date_year_only;
```


```SQL
-- Unique response_units (135 of them) with number of calls for each in the dataset
-- ordered by response_unit name
-- Use to help determine which response_unit names may be ignored
SELECT response_unit, count(response_unit) total_call_count
   FROM 'emergency_calls' 
   GROUP BY response_unit
   ORDER BY response_unit;
```


```SQL
-- Unique response_units (135 of them) with number of calls for each in the dataset
-- ordered by response_unit name
-- Use to help determine which response_unit names may be ignored
SELECT response_unit, count(response_unit) total_call_count
   FROM 'emergency_calls' 
   GROUP BY response_unit
   ORDER BY total_call_count DESC;
```


```SQL
-- average incident response times and in-service times 
-- for specified response_units for all years in the dataset.
-- total_call_count is included to help sanity check avg_time_in_service_in_seconds values.
SELECT incident_date_year_only, response_unit, count(response_unit) total_call_count, 
CAST(AVG(response_time_in_seconds) AS INTEGER) AS avg_response_time_in_seconds_integer, 
CAST(AVG(time_in_service_in_seconds) AS INTEGER) AS time_in_service_in_seconds_integer
   FROM 'emergency_calls' 
   WHERE (response_unit IN ('M1', 'M2', 'M3', 'M5', 'M6', 'M7', 'M8', 'M10', 'M21', 'M24', 'M25', 'MALC1', 'MALC10', 'MWM31', 'MALC2'))
   AND (call_type IN ('FIREC', 'GRASFIRE', 'RSALARM', 'ECHO', 'CARFIRE', 'MEDC', 'MEDD', 'MEDE'))
   GROUP BY incident_date_year_only, response_unit
   ORDER BY response_unit, incident_date_year_only;
```


```SQL
-- List every call_type, the number of incidents for each call type, 
-- the average response_time_in_seconds and the average time_in_service_in_seconds
-- for each call type.  [556 rows returned]
SELECT DISTINCT call_type, count(call_type) total_call_type_count,
CAST(AVG(response_time_in_seconds) AS INTEGER) AS avg_response_time_in_seconds_integer, 
CAST(AVG(time_in_service_in_seconds) AS INTEGER) AS time_in_service_in_seconds_integer
   FROM 'emergency_calls' 
   -- WHERE response_unit = 'M1'
   GROUP BY call_type
   ORDER BY total_call_type_count DESC;
```


```SQL
-- Unique response_units (135 of them) with number of calls for each in the dataset
-- ordered by response_unit name
-- Use to help determine which response_unit names may be ignored
SELECT response_unit, count(response_unit) total_call_count
   FROM 'emergency_calls' 
   GROUP BY response_unit
   ORDER BY total_call_count DESC;
```


* How best to identify the mean for columns and for grouped values?  

One approach for whole columns is:  
```SQL
-- This gets the median (the element in the middle of an ordered list)
-- of the response_time_in_seconds column of the emergency_calls table 
SELECT response_time_in_seconds
FROM 'emergency_calls' 
ORDER BY response_time_in_seconds
LIMIT 1
OFFSET (SELECT COUNT(response_time_in_seconds)
        FROM 'emergency_calls') / 2
```
Result median response_time_in_seconds = 695  


```SQL
-- This gets the median (the element in the middle of an ordered list)
-- of the time_in_service_in_seconds column of the emergency_calls table 
SELECT time_in_service_in_seconds
FROM 'emergency_calls' 
ORDER BY time_in_service_in_seconds
LIMIT 1
OFFSET (SELECT COUNT(time_in_service_in_seconds)
        FROM 'emergency_calls') / 2

```
Result median time_in_service_in_seconds = 3141  


What about getting the median for a subset of a column (GROUP BY or PARTITION)?
This looks like a potential model: https://stackoverflow.com/questions/65212352/calculating-median-in-sqlite  
https://dbfiddle.uk/loGSXFZ3  

https://www.sqlitetutorial.net/

-----


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
SQLite Documentation
https://www.sqlite.org/docs.html
https://sqlite.org/pragma.html#pragma_index_info  
Built-in Aggregate Functions  
https://www.sqlite.org/lang_aggfunc.html  
SQLite: Combining the AND and OR Conditions
https://www.techonthenet.com/sqlite/and_or.php
SQLite GROUP BY Clause
https://sqldocs.org/sqlite-database/sqlite-group-by/
SQLite Group By: Mastering Data Aggregation in SQL Databases
https://www.sql-easy.com/learn/sqlite-group-by/
SQLite DISTINCT Query
https://sqldocs.org/sqlite-database/sqlite-distinct/

Built-In Scalar SQL Functions
https://www.sqlite.org/lang_corefunc.html
Window Functions
https://www.sqlite.org/windowfunctions.html

### Random SQL Notes:  
```SQL
PRAGMA table_list;
PRAGMA table_list(emergency_calls);
PRAGMA main.table_info(emergency_calls);
PRAGMA main.table_xinfo(emergency_calls);
PRAGMA main.index_list(emergency_calls);

SELECT COUNT(*) FROM emergency_calls
SELECT * FROM 'emergency_calls' LIMIT 0,200
SELECT * FROM 'emergency_calls' WHERE incident_date < "2010-01-02" LIMIT 0,200
SELECT * FROM 'emergency_calls' WHERE incident_date < "2010-01-02" OR incident_date > "2010-01-02" LIMIT 0,60
SELECT * FROM 'emergency_calls' WHERE incident_date > "2010-01-01" AND incident_date < "2010-01-03" LIMIT 0,60
SELECT * FROM 'emergency_calls' WHERE incident_date_year_only = 2012 LIMIT 0,60
SELECT * FROM 'emergency_calls' WHERE dispatch_time < "09:51:59" LIMIT 0,200

-- The following emits the number of calls (any call_type) per unit over the entire db scope
-- ordered by response_unit
SELECT response_unit, count(call_type)
   FROM emergency_calls
   GROUP BY response_unit

-- The following emits the number of distinct call_types per unit over the entire db scope
-- ordered by call_type_count
SELECT response_unit, count(DISTINCT call_type) AS call_type_count
   FROM emergency_calls
   GROUP BY response_unit
   ORDER BY call_type_count;

-- The following emits the number of distinct_call_types, total_call_count (any call_type) per unit over the entire db scope
-- This may help identify (then weed out) some noise in the data.
-- For example, should be "care about" a response_unit that has one call over 10 years? ...2? ...4? 
-- What is the threshold below which we ignore given response_unit's records?
SELECT response_unit, count(DISTINCT call_type) AS distinct_call_types, count(response_unit) AS total_call_count
   FROM emergency_calls
   GROUP BY response_unit
   ORDER BY distinct_call_types;
   
-- The following emits the number of distinct_call_types, total_call_count (any call_type) per unit over the entire db scope
-- ordered by the response_unit name.  This may be easier for some to navigate.  The question remains, 
-- What is the num. of calls threshold below which we ignore given response_unit's records?
-- This may help identify (then weed out) some noise in the data.
SELECT response_unit, count(DISTINCT call_type) AS distinct_call_types, count(response_unit) AS total_call_count
   FROM emergency_calls
   GROUP BY response_unit
   ORDER BY response_unit;

-- The following emits each unit and a list of all the call_types in their records
SELECT response_unit, GROUP_CONCAT(call_type) AS call_types
   FROM emergency_calls
   GROUP BY response_unit
   HAVING MIN(call_type) <> MAX(call_type);

-- What call types are the longest for teams?
SELECT response_unit, call_type, time_in_service
   FROM emergency_calls
   WHERE time_in_service > "01:30:00"
   GROUP BY call_type

-- What call types are the longest, and how long is each call of that type?
SELECT call_type, GROUP_CONCAT(time_in_service)
    FROM emergency_calls
    WHERE time_in_service > "01:45:00"
    GROUP BY call_type
    ORDER BY call_type

-- What call types do each of the units serve?
SELECT call_type, GROUP_CONCAT(response_unit)
    FROM emergency_calls
    GROUP BY call_type
    ORDER BY call_type

-- The following emits each unit and a list of all the call_types in their records by date
-- This illustrates which units are dealing with more calls per day
SELECT response_unit, count(call_type)
   FROM emergency_calls
   GROUP BY response_unit
-- or 
SELECT incident_date, response_unit, GROUP_CONCAT(call_type) AS call_types
   FROM emergency_calls
   GROUP BY response_unit

-- incident_date","response_unit","call_type","dispatch_time","enroute_time","arrive_time","time_in_service"
```


