import csv
import json
import os

class CSVDataTable:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_dir = dir_path + "/Data/"
    # t_name: The "Name" of the collection.
    # t_file: The name of the CSV file. The class looks in the data_dir for the file.
    headers = []
    data = []

    def __init__(self, t_name, t_file, key_columns):
        self.t_name = t_name
        self.t_file = t_file
        self.key_columns = key_columns

    # Pretty print the CSVTable and its attributes.
    def __str__(self):
        s = ""
        d = self.data[0]
        for key in d:
            s = s + key.center(6)
        s = s + "\n"
        for row in self.data:
            for key in row:
                s = s + row[key].center(6)
            s = s + "\n"
        return s

    # loads the data from the file into the class instance data.
    # You decide how to store and represent the rows from the file.
    def load(self):
        try:
            self.data = []
            with open(self.data_dir + self.t_file) as csvfile:
                reader = csv.DictReader(csvfile)
                count = 1
                for row in reader:
                    # Return an error if the specified primary key fields for the DataTable are
                    # not a subset of the columns in the underlying file/table.
                    if count == 1:
                        for key in self.key_columns:
                            if key not in row:
                                raise ValueError("the specified primary key fields are not a subset of the columns "
                                                 "in the file/table")
                        count = 2
                    self.data.append(row)
        except ValueError as e:
            print(e)

    def save(self):
        self.headers = []
        d = self.data[0]
        for key in d:
            self.headers.append(key)
        with open(self.data_dir + self.t_file, 'w', newline="") as f:
            f_scv = csv.DictWriter(f, self.headers)
            f_scv.writeheader()
            f_scv.writerows(self.data)

    def find_by_primary_key(self, s, fields=None):
        try:
            if len(self.data) == 0:
                raise ValueError("Data Load Fails")
            # Check if fields contains attributes that don't exist
            if fields is not None:
                d = self.data[0]
                for key in fields:
                    if key not in d:
                        raise ValueError("The fields have attributes that don't exist in table")
            ans = {}
            for row in self.data:
                flag = True
                for i in range(len(self.key_columns)):
                    if row[self.key_columns[i]] != s[i]:
                        flag = False
                        break
                if flag:
                    if fields is None:
                        return row
                    for field in fields:
                        ans[field] = row[field]
                    return ans
        except ValueError as e:
            print(e)

    # The input is:
    # t: The template to match. The result is a list of rows
    # whose attribute/value pairs exactly match the template.
    # fields: A subset of the fields to include for each result.
    # Raises an exception if the template or list of fields contains
    # a column/attribute name not in the file.
    def find_by_template(self, t, fields=None):
        ans = []
        try:
            if len(self.data) == 0:
                raise ValueError("Data Load Fails")
            # Check if the search condition has attributes that don't exist in table
            dic = self.data[0]
            for k in t:
                if k not in dic:
                    raise ValueError("search condition t has attributes that don't exist in table")
            # Check if fields contains attributes that don't exist
            if fields is not None:
                if len(fields) == 0:
                    raise ValueError("the input fields can't be an empty list")
                for k in fields:
                    if k not in dic:
                        raise ValueError("fields have attributes that don't exist in table")
            # Perform search
            for row in self.data:
                flag = False
                for key in t:
                    if t[key] != row[key]:
                        flag = True
                        break
                if flag:
                    continue
                temp = {}
                if fields is None:
                    ans.append(row)
                else:
                    for key in fields:
                        temp[key] = row[key]
                    ans.append(temp)
            return ans
        except ValueError as e:
            print(e)

    # Inserts the row into the table.
    # Raises on duplicate key or invalid columns.
    def insert(self, r):
        try:
            if len(self.data) == 0:
                raise ValueError("Data Load Fails")
            # Check the new row has all primary keys
            for key_column in self.key_columns:
                if key_column not in r:
                    raise ValueError("Lack of primary key, break integrity constraint")
            # Check if new row has duplicate primary key
            for row in self.data:
                flag = True
                for key in self.key_columns:
                    if r[key] != row[key]:
                        flag = False
                if flag:
                    raise ValueError("Duplicate Key")
            # Check if primary keys are null
            for key in r:
                if key in self.key_columns:
                    if len(r[key]) == 0:
                        raise ValueError("Primary keys are null")
            # Check if the new row has attributes that don't exist in table
            dic = self.data[0]
            for k in r:
                if k not in dic:
                    raise ValueError("The column has attributes that don't exist in table")

            # if the new row lacks of some attributes, set values of these attributes to "0"
            d = self.data[0]
            for k in d:
                if k not in r:
                    r[k] = "0"
            # insert the new row into table
            self.data.append(r)
        except ValueError as e:
            print(e)

    # t: A template.
    # Deletes all rows matching the template.
    def delete(self, t):
        try:
            if len(self.data) == 0:
                raise ValueError("Data Load Fails")
            # Check if the search condition has attributes that don't exist in table
            dic = self.data[0]
            for k in t:
                if k not in dic:
                    raise ValueError("The delete condition has attributes that don't exist in table")
            for row in self.data:
                flag = False
                for key in t:
                    # if key not in row:
                    #     raise Error("Error")
                    if t[key] != row[key]:
                        flag = True
                        break
                if flag:
                    continue
                self.data.remove(row)
        except ValueError as e:
            print(e)


#
# csvTable = CSVDataTable("batting", "People.csv", ["curry"])
# csvTable.load()
# ans = csvTable.__str__()
# print(ans[0:1000])
# csvTable.delete({"playerID": "liuyu123"})
# csvTable.save()
# ans = csvTable.find_by_template({"playerID": "liuyu123"})
# print("ans=", json.dumps(ans, indent=2))
# ans = csvTable.find_by_template({"playerID": "aardsda01d"}, {})

# for r in ans:
#     print(r)
# csvTable.__str__()
# li = csvTable.find_by_template({"playerID": "", "birthCountry": "USA"}, {"playerID"})
# for row in li:
#     print(row)
# csvTable.__str__()
# csvTable.greater()
# csvTable.__str__()
# dic = {"ddd": "e", "dgg": "rg"}
# for k in dic:
#     print(k)
