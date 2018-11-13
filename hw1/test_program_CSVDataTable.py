from CSVDataTable import CSVDataTable
import json

# Initialize the Batting table
batting_csvtable = CSVDataTable("batting", "Batting.csv", ["playerID", "teamID", "yearID", "stint"])
batting_csvtable.load()

# Test load
# the specified primary key fields for the DataTable are not a subset of the columns in the underlying file/table
# batting_csvtable = CSVDataTable("batting", "Batting.csv", ["playersff", "teamID", "yearID", "stint"])
# batting_csvtable.load()

# Test find_by_primary_key
# If the fields is None
ans = batting_csvtable.find_by_primary_key(["abbeych01", "WAS", "1897", "1"])
print(json.dumps(ans, indent=2))
# If the fields is not None
ans = batting_csvtable.find_by_primary_key(["abbeych01", "WAS", "1897", "1"], ["playerID", "lgID", "G", "BB", "SH"])
print(json.dumps(ans, indent=2))
# If the fields has values that don't exist in csv file, in the case, I use "CCCCC" to test my program
ans = batting_csvtable.find_by_primary_key(["abbeych01", "WAS", "1897", "1"], ["playerID", "lgID", "G", "BB", "CCCCC"])
print(json.dumps(ans, indent=2))


# Test find_by_template
# If the input t is correct and fields is None
ans = batting_csvtable.find_by_template({"teamID": "CHN", "yearID": "2006"})
print(json.dumps(ans, indent=2))
# If the input t is correct and fields is not None
ans = batting_csvtable.find_by_template({"teamID": "CHN", "yearID": "2006"}, ["playerID", "yearID", "teamID",
                                                                              "RBI", "G"])
print(json.dumps(ans, indent=2))
# If the input t is incorrect and fields is correct, In this case, "teamId" is not a attribute in csv
ans = batting_csvtable.find_by_template({"teamId": "CHN", "yearID": "2006"}, ["playerID", "yearID", "teamID",
                                                                               "RBI", "G"])
print(json.dumps(ans, indent=2))
# If the input t is correct and fields is incorrect, In this case, "playerId" is not a attribute in csv
ans = batting_csvtable.find_by_template({"teamID": "CHN", "yearID": "2006"}, ["playerId", "yearID", "teamID",
                                                                             "RBI", "G"])
print(json.dumps(ans, indent=2))
# If the input t is correct and fields is an empty list, In this case, fields is []
ans = batting_csvtable.find_by_template({"teamID": "CHN", "yearID": "2006"}, [])
print(json.dumps(ans, indent=2))

# Test insert
# the insert statement is correct
batting_csvtable.insert({"playerID": "yl3957", "teamID": "CHN", "yearID": "2018", "stint": "1", "AB": "100", "G": "10"})
ans = batting_csvtable.find_by_template({"playerID": "yl3957"})
print(json.dumps(ans, indent=2))
# the insert statement t lacks of primary keys, in this case, t doesn't have "teamID"
batting_csvtable.insert({"playerID": "yl3957", "yearID": "2018", "stint": "1", "AB": "100", "G": "10"})
# if the new row has same key as one row has in csv file, in this case, ("aardsda01","SFN", "2004", "1")
# already exists in csv file
batting_csvtable.insert({"playerID": "aardsda01", "teamID": "SFN", "yearID": "2004", "stint": "1", "AB": "100"})
# If t has attributes that don't exist in csv file, in this case, "CCCCC" doesn't exist in csv file
batting_csvtable.insert({"playerID": "aardsda01", "teamID": "CHN", "yearID": "2004", "stint": "1", "CCCCC": "100"})
# If t has primary keys that are null
batting_csvtable.insert({"playerID": "aardsda01", "teamID": "", "yearID": "2004", "stint": "1"})

# test delete
# If the deletion statement t is correct
batting_csvtable.delete({"playerID": "aardsda01", "yearID": "2004", "stint": "1"})
ans = batting_csvtable.find_by_template({"playerID": "aardsda01", "yearID": "2004", "stint": "1"})
print(ans)
# If the deletion statement t has attributes that don't exist in csv file, in thiis case, "CCCCC" doesn't exist in file
batting_csvtable.delete({"playerID": "aardsda01", "yearID": "2004", "stint": "1", "CCCCC": "sss"})

# test save()
# insert one row to csv file and save the data into csv file, then load csv file again and insert the same row as
# before, the program will raise an error because duplicate key, finally print the new row
batting_csvtable.insert({"playerID": "yl3957", "teamID": "MUL", "yearID": "2018", "stint": "1", "AB": "100"})
batting_csvtable.save()
batting_csvtable.load()
batting_csvtable.insert({"playerID": "yl3957", "teamID": "MUL", "yearID": "2018", "stint": "1", "AB": "100"})
ans = batting_csvtable.find_by_template({"playerID": "yl3957"})
print(json.dumps(ans, indent=2))

# delete the new row and print the row
batting_csvtable.delete({"playerID": "yl3957", "teamID": "MUL", "yearID": "2018", "stint": "1", "AB": "100"})
batting_csvtable.save()
batting_csvtable.load()
ans = batting_csvtable.find_by_template({"playerID": "yl3957"})
print(json.dumps(ans, indent=2))
