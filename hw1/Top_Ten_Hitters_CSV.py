import csv
import os

def top_ten_hitters():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data = []
    with open(dir_path + "/Data/" + "Batting.csv") as csvfile:
        temp = csv.DictReader(csvfile)
        for r in temp:
            data.append(r)
    t = []
    with open(dir_path + "/Data/" + "People.csv") as csvfile:
        temp = csv.DictReader(csvfile)
        for r in temp:
            t.append(r)
    hashtable = {}
    for row in t:
        hashtable[row["playerID"]] = [row["nameFirst"], row["nameLast"]]
    dic = {}
    players = []
    for r in data:
        if r["playerID"] in dic:
            dic[r["playerID"]].append(r)
        else:
            dic[r["playerID"]] = [r]
    for people in dic:
        flag = False
        ab = 0
        h = 0
        first_year = 2020
        last_year = 0
        for row in dic[people]:
            if int(row["yearID"]) >= 1960:
                flag = True
            first_year = min(first_year, int(row["yearID"]))
            last_year = max(last_year, int(row["yearID"]))
            if row["H"] == "":
                continue
            h = h + int(row["H"])
            ab = ab + int(row["AB"])
        if flag:
            if ab == 0 or ab <= 200:
                continue
            average = h / ab
            k = dict()
            k["playerId"] = people
            k["career_average"] = average
            k["first_name"] = hashtable[people][0]
            k["last_name"] = hashtable[people][1]
            k["career_hits"] = h
            k["career_at_bats"] = ab
            k["first_year"] = first_year
            k["last_year"] = last_year
            players.append(k)
    players.sort(key=lambda x: x['career_average'], reverse=True)
    count = 0
    ans = []
    while count < 10:
        print(players[count])
        ans.append(players[count])
        count = count + 1
    return ans

# The function prints top ten hitters and it also returns a list which contains top ten hitters
top_ten_hitters()

