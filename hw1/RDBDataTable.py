import pymysql.cursors
import json
import pandas as pd


class RDBDataTable:
    # t_name: The "Name" of the collection.
    # t_file: The name of the CSV file. The class looks in the data_dir for the file.
    cursor = None
    cnx = None

    def __init__(self, t_name, t_file, key_columns):
        # you should configure MySQL connection again
        self.cnx = pymysql.connect(host='localhost',
                                   user='root',
                                   password='root',
                                   db='db_homework',
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.cnx.cursor()
        self.t_name = t_name
        self.t_file = t_file
        self.key_columns = key_columns

    def __str__(self):
        q = "SELECT * FROM " + self.t_name
        self.cursor.execute(q)
        r = self.cursor.fetchall()
        s = ""
        d = r[0]
        for key in d:
            s = s + key.center(6)
        s = s + "\n"
        for row in r:
            for key in row:
                s = s + str(row[key]).center(6)
            s = s + "\n"
        return s

    def load(self):
        pass

    def save(self):
        pass

    # The input is:
    # t: The template to match. The result is a list of rows
    # whose attribute/value pairs exactly match the template.
    # fields: A subset of the fields to include for each result.
    # Raises an exception if the template or list of fields contains
    # a column/attribute name not in the file.
    def find_by_primary_key(self, s, fields=None):
        ans = []
        q = "SELECT "
        where = ""
        select = ""
        try:
            if fields is not None:
                if len(fields) == 0:
                    raise Exception("fields can't be an empty list")
                for key in fields:
                    select = select + key + ","
                    # print(select)
                q = q + select[0: len(select) - 1] + " " + "FROM " + self.t_name + " " + "WHERE "
            else:
                q = q + "* FROM " + self.t_name + " WHERE "

            for i in range(len(self.key_columns)):
                where = where + self.key_columns[i] + " = " + "'" + s[i] + "'" + " and "
            q = q + where[0: len(where) - 5]
            self.cursor.execute(q)
            r = self.cursor.fetchall()
            return r
        except Exception as e:
            print(e)

    def find_by_template(self, t, fields=None):
        q = "SELECT "
        where = ""
        select = ""
        try:
            if fields is not None:
                if len(fields) == 0:
                    raise Exception("fields can't be an empty list")
                for key in fields:
                    select = select + key + ","
                    # print(select)
                q = q + select[0: len(select)-1] + " " + "FROM " + self.t_name + " " + "WHERE "
            else:
                q = q + "* FROM " + self.t_name + " WHERE "
            for key in t:
                where = where + key + " = " + "'" + t[key] + "'" + " and "
            q = q + where[0: len(where) - 5]
            self.cursor.execute(q)
            r = self.cursor.fetchall()
            return r
        except Exception as e:
            print(e)

    # Inserts the row into the table.
    # Raises on duplicate key or invalid columns.
    def insert(self, r):
        try:
            q = "INSERT INTO " + self.t_name + " "
            key = ""
            value = ""
            for k in r:
                key = key + k + ","
                value = value + "'" + r[k] + "'" + ","
            keys = "(" + key[0: len(key)-1] + ")"
            values = "(" + value[0: len(value) - 1] + ")"
            q = q + keys + " VALUES " + values + ";"
            self.cursor.execute(q)
            self.cnx.commit()
        except Exception as e:
            print(e)

    # t: A template.
    # Deletes all rows matching the template.
    def delete(self, t):
        try:
            q = "DELETE FROM " + self.t_name + " WHERE "
            where = ""
            for key in t:
                where = where + key + " = " + "'" + t[key] + "'" + " and "
            w = where[0: len(where)-5]
            q = q + w
            self.cursor.execute(q)
            self.cnx.commit()
        except Exception as e:
            print(e)


# csvTable = RDBDataTable("batting", "Batting.csv", ["playerID", "teamID", "yearID", "stint"])
# print(csvTable.__str__()[1:1000])
# ans = csvTable.find_by_primary_key(["aardsda01", "CHN", "2006", "1"])
# print(ans)
# csvTable.insert({"playerID": "ly777", "nameFirst": "Yu", "nameLast": "Liu"})
# li = csvTable.find_by_template({"birthYear": "'1981'", "birthCountry": "'USA'"}, {"playerID"})
# csvTable.delete({"playerID": "ly777"})
# li = csvTable.find_by_template({"playerID": "ly777"}, {"playerID"})
# csvTable.greater()
# csvTable.__str__()

