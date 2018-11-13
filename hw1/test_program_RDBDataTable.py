from RDBDataTable import RDBDataTable
import json

# Initialize the Batting table
batting_rdbtable = RDBDataTable("batting", "Batting.csv", ["playerID", "teamID", "yearID", "stint"])

# Test find_by_primary_key
# If the fields is None
ans = batting_rdbtable.find_by_primary_key(["abbeych01", "WAS", "1897", "1"])
print(json.dumps(ans, indent=2))
# If the fields is not None
ans = batting_rdbtable.find_by_primary_key(["abbeych01", "WAS", "1897", "1"], ["playerID", "lgID", "G", "BB", "SH"])
print(json.dumps(ans, indent=2))
# If the fields has values that don't exist in csv file, in the case, I use "CCCCC" to test my program
ans = batting_rdbtable.find_by_primary_key(["abbeych01", "WAS", "1897", "1"], ["playerID", "lgID", "G", "BB", "CCCCC"])
print(json.dumps(ans, indent=2))

# Test find_by_template
# If the input t is correct and fields is None
ans = batting_rdbtable.find_by_template({"teamID": "CHN", "yearID": "2006"})
print(json.dumps(ans, indent=2))
# If the input t is correct and fields is not None
ans = batting_rdbtable.find_by_template({"teamID": "CHN", "yearID": "2006"}, ["playerID", "yearID", "teamID",
                                                                              "RBI", "G"])
print(json.dumps(ans, indent=2))
# If the input t is incorrect and fields is correct, In this case, "teamIs" is not a attribute in csv
ans = batting_rdbtable.find_by_template({"teamIs": "CHN", "yearID": "2006"}, ["playerID", "yearID", "teamID",
                                                                               "RBI", "G"])
print(json.dumps(ans, indent=2))
# If the input t is correct and fields is incorrect, In this case, "playerIs" is not a attribute in csv
ans = batting_rdbtable.find_by_template({"teamID": "CHN", "yearID": "2006"}, ["playerIs", "yearID", "teamID",
                                                                             "RBI", "G"])
print(json.dumps(ans, indent=2))
# If the input t is correct and fields is an empty list, In this case, fields is []
ans = batting_rdbtable.find_by_template({"teamID": "CHN", "yearID": "2006"}, [])
print(json.dumps(ans, indent=2))

# Test insert
# the insert statement is correct
batting_rdbtable.insert({"playerID": "aardsda01", "teamID": "CHN", "yearID": "2018", "stint": "1", "AB": "100", "G": "10"})
ans = batting_rdbtable.find_by_template({"playerID": "aardsda01", "teamID": "CHN", "yearID": "2018", "stint": "1", "AB": "100", "G": "10"})
print(json.dumps(ans, indent=2))
# the insert statement t lacks of primary keys, in this case, t doesn't have "teamID"
batting_rdbtable.insert({"playerID": "aardsda01", "yearID": "2018", "stint": "1", "AB": "100", "G": "10"})
# if the new row has same key as one row has in csv file, in this case, ("aardsda01","SFN", "2004", "1")
# already exists in csv file
batting_rdbtable.insert({"playerID": "aardsda01", "teamID": "SFN", "yearID": "2004", "stint": "1", "AB": "100"})
# If t has attributes that don't exist in csv file, in this case, "CCCCC" doesn't exist in csv file
batting_rdbtable.insert({"playerID": "aardsda01", "teamID": "CHN", "yearID": "2004", "stint": "1", "CCCCC": "100"})

# test delete
# If the deletion statement t is correct
batting_rdbtable.delete({"playerID": "aardsda01", "yearID": "2004", "stint": "1"})
ans = batting_rdbtable.find_by_template({"playerID": "aardsda01", "yearID": "2004", "stint": "1"})
print(json.dumps(ans, indent=2))
# If the deletion statement t has attributes that don't exist in csv file, in thiis case, "CCCCC" doesn't exist in file
batting_rdbtable.delete({"playerID": "aardsda01", "yearID": "2004", "stint": "1", "CCCCC": "sss"})
