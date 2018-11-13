1. CSVDataTable
Explanation for code
In CSVDataTable class, there are eight methods.
a. __init__: The function has three parameters including t_name, t_file and key_columns.
I used this function to store the name of database, the name of csv file and primary keys of the table.
b. __str__: Used to print the whole cvs file by row.
c. load: I used this function to open the csv file and read data from csv file. Then I store data from csv file into a global variable called data. Global variable 
data is a list, which contains many dictionaries, each dictionary is a row in csv file.
d. save: I saved global variable data into csv file. 
e. find_by_primary_key: Firstly I wrote code to check if variable fields contains attributes that don't exist in the csv file. Then I loop the global variable data
by row to check which row matches the search condition.
f. find_by_template: Firstly I wrote code to check if t or fields has attributes that don't exist in csv files. Then I loop each dictionary in global variable data to 
check which dictionary satisfies the t. Then I select parts of (key, value) pairs in relevant dictionaries according to variable fields to construct new dictionaries.
Finally, I put these new dictionaries into a list.
g. inset: Firstly, I wrote to check if t contains all primary keys and t contains some attributes that don't exist in csv file. Then I check if the primary key of new row 
are duplicate key in csv file. I check if t lacks of some attributes and relevant values, then I add these attributes with value "0" to the new dictionary.
h. delete: Firstly, I wrote to check if t contains some attributes that don't exist in csv file. Then I loop global variable data to find dictionaries matching t. Then I  
remove these dictionaries from data.

Explanation for running code
Firstly, you should create a new CSVDataTable object by passing the name of database, the name of csv file and primary keys of the table into constructor.
Then you can use the object to call any methods you want.

2. RDBDataTable
Explanation for code
In this class, I try to construct SQL strings for each method. 
for find_by_primary_key: I try to construct SQL SELCET (fields[0], fields[1],...) FROM table_name WHERE primary_key_1=s[0] and primary_key_2=s[1] and ...
for find_by_template: I try to construct SQL SELCET (fields[0], fields[1],...) FROM table_name WHERE key1=t[key1] and key2=t[key2] and ...
for insert: I try to construct SQL INSERT INTO table_name (key1, key2, ...) VALUES (t[key1], t[key2], ...)
for delete: I try to construct SQL DELETE FROM table_name WHERE key1=t[key1] and key2=t[key2] and ...

Explanation for running code
Firstly, you should create a new RDBDataTable object by passing the name of database, the name of csv file and primary keys of the table into constructor.
Then you should configure the MySQL connection. Next you can use the object to call any methods you want.

3. Top-Ten-Hitters
a. CSV Implementation 
Firstly, I loop Batting.csv and use dictionary to store records of each person as (playerID, [record1, record2, ...]) pair. Then I loop the new dictionary to check if 
a player has yearID that is greater than or equal to 1960 and calculate the sum of H and the sum of AB. If the person has a yearID which >=1960, I caculate the 
averate by (the sum of H/the sum of AB). Then I contruct a new dictionary and put it into a list. After looping all players, I sort the list based on average. Finally, 
return first 10 players.
b. RDB Implementation
I directly use the SQL in Courseworks.

4. My chosen correctness:
(1). Test load
a. If the specified primary key fields for the DataTable are not a subset of the columns in the underlying file/table, the  program raises an error

(2). Test find_by_primary_key
a. If the fields is None and s is correct, the program should return relevant results
b. If the fields is not None and s is correct, the program should return relevant results
c. If the fields has values that don't exist in csv file and s is correct, the program should raise an error

(3). Test find_by_template
a. If the input t is correct and fields is None, the program should return relevant results
b. If the input t is correct and fields is not None, the program should return relevant results
c. If the input t is incorrect and fields is correct, the program should raise an error
d. If the input t is correct and fields is incorrect, the program should raise an error
e. If the input t is correct and fields is an empty list, the program should raise an error

(4). Test insert
a. If insert statement is correct, the program should return relevant results
b. If insert statement t lacks of primary keys, the program should raise an error
c. if the new row has same primary key as one row has in csv file, the program should raise an error
d. If t has attributes that don't exist in csv file,the program should raise an error
e. If t has primary keys that are null, the program should raise an error

(5). Test delete
a. If the deletion statement t is correct
b. If the deletion statement t has attributes that don't exist in csv file, the program should raise an error

