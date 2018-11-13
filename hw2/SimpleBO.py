import pymysql
import json
import copy

cnx = pymysql.connect(host='localhost',
                              user='dbuser',
                              password='dbuser',
                              db='lahman2017raw',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)


def run_q(q, args, fetch=False):
    cursor = cnx.cursor()
    cursor.execute(q, args)
    if fetch:
        result = cursor.fetchall()
    else:
        result = None
    cnx.commit()
    return result


def template_to_where_clause(t):
    s = ""

    if t is None:
        return s
    for (k, v) in t.items():
        if s != "":
            s += " AND "
        s += k + "='" + v[0] + "'"

    if s != "":
        s = "WHERE " + s

    return s


def find_primary_key(table):
    q = "SELECT column_name FROM INFORMATION_SCHEMA.`KEY_COLUMN_USAGE` WHERE table_name=" + "'" + table + "'" + \
        "AND CONSTRAINT_SCHEMA='lahman2017raw' AND constraint_name='PRIMARY'"
    m = run_q(q, None, True)
    primary_keys = []
    for i in m:
        primary_keys.append(i["column_name"])
    return primary_keys


def find_by_template(table, template, fields=None, offset=0, limit=10):

    wc = template_to_where_clause(template)
    q = "select " + (fields[0] if fields is not None else "*") + " from " + table + " " + wc + " " + "limit " + str(limit) \
        + " " + "OFFSET " + str(offset)
    result = run_q(q, None, True)

    res = {}
    res['data'] = result
    s = "/api/" + table
    if template is not None:
        s += "?"
        for k, v in template.items():
            s += k + "=" + v[0] + "&"
        s = s[0:len(s)-1]
    if fields is not None:
        if template is None:
            s += "?fields="
        else:
            s += '&fields='
        for l in fields:
            s += l + ","
        s = s[0:len(s)-1]
    if template is None and fields is None:
        s += "?"
    else:
        s += "&"
    res['links'] = []
    if int(offset) - int(limit) >= 0:
        pre = {"previous": s + "offset=" + str(offset - limit) + "&limit=" + str(limit)}
        res['links'].append(pre)
    cur = {"current": s + "offset=" + str(offset) + "&limit=" + str(limit)}
    res['links'].append(cur)
    pos = {"next": s + "offset=" + str(offset + limit) + "&limit=" + str(limit)}
    res['links'].append(pos)

    return res


def find_by_primary_key(table, primary_key, fields=None, offset=0, limit=10):

    p = find_primary_key(table)
    v = primary_key.split("_")
    dic = {}
    for i in range(len(p)):
        dic[p[i]] = [v[i]]
    wc = template_to_where_clause(dic)
    q = "select " + (fields[0] if fields is not None else "*") + " from " + table + " " + wc + " " + "limit " + str(limit) \
        + " " + "OFFSET " + str(offset)
    result = run_q(q, None, True)
    res = {}
    res['data'] = result
    s = "/api/" + table + "/" + primary_key
    if fields is not None:
        s += "?fields="
        for l in fields:
            s += l + ","
        s = s[0:len(s) - 1]
    if fields is None:
        s += "?"
    else:
        s += "&"
    res['links'] = []
    if int(offset) - int(limit) >= 0:
        pre = {"previous": s + "offset=" + str(offset - limit) + "&limit=" + str(limit)}
        res['links'].append(pre)
    cur = {"current": s + "offset=" + str(offset) + "&limit=" + str(limit)}
    res['links'].append(cur)
    pos = {"next": s + "offset=" + str(offset + limit) + "&limit=" + str(limit)}
    res['links'].append(pos)

    return res


def insert(table, r):
    keys = ""
    values = ""
    for k, v in r.items():
        keys += k + ','
        values += "'" + v + "',"
    q = "INSERT INTO " + table + "(" + keys[:len(keys) - 1] + ") VALUES" + "(" + values[:len(values) - 1] + \
        ")"
    run_q(q, None, False)


def delete(table, t):
    p = find_primary_key(table)
    v = t.split("_")
    dic = {}
    for i in range(len(p)):
        dic[p[i]] = [v[i]]
    q = "DELETE FROM " + table + " WHERE "
    where = ""
    for key in dic:
        where = where + key + " = " + "'" + dic[key][0] + "'" + " and "
    w = where[0: len(where)-5]
    q = q + w
    run_q(q, None, False)


def roster(t, offset=0, limit=10):

    wc = template_to_where_clause(t)
    q = "select x.nameLast, x.nameFirst, x.playerID, x.teamID, x.yearID, x.G as g_all, x.H as hits, x.AB as abs, f.attempts,\
    f.errors from (select nameLast, nameFirst, p.playerID, teamID, yearID, G, H, AB \
    from batting as b join people as p on b.playerID = p.playerID " + wc + ") as x \
    join (select playerID, yearID, teamID, sum(A) as attempts, sum(E) as errors from fielding " + wc + "\
    group by playerID ) as f \
    on x.playerID = f.playerID" + " " + " limit " + str(limit) + " offset " + str(offset)
    result = run_q(q, None, True)
    res = {}
    res['data'] = result
    s = "/api/roster"
    if t is not None:
        s += "?"
        for k, v in t.items():
            s += k + "=" + v[0] + "&"
        s = s[0:len(s)-1]
    if t is None:
        s += "?"
    else:
        s += "&"
    res['links'] = []
    if int(offset) - int(limit) >= 0:
        pre = {"previous": s + "offset=" + str(offset - limit) + "&limit=" + str(limit)}
        res['links'].append(pre)
    cur = {"current": s + "offset=" + str(offset) + "&limit=" + str(limit)}
    res['links'].append(cur)
    pos = {"next": s + "offset=" + str(offset + limit) + "&limit=" + str(limit)}
    res['links'].append(pos)
    return res


def find_rows_by_career_stas_by_playerid(t, offset=0, limit=10):

    q = "select b.playerID, b.teamID, b.yearID, b.G as g_all, b.H as hits, b.AB as ABs, f.A as Assits,f.E as errors " \
        "from batting as b join " \
        "(select fielding.playerID, fielding.teamID, fielding.yearID, fielding.stint, sum(fielding.A) as A, sum(fielding.E) as E from fielding " \
        "group by playerID, teamID, yearID, stint) as f on b.playerID = f.playerID and b.teamID = f.teamID and b.yearID = f.yearID and b.stint = f.stint " \
        "where b.playerID = " + "'" + t + "'" + " limit " + str(limit) + " offset " + str(offset)
    result = run_q(q, None, True)
    res = {}
    res['data'] = result
    s = "/api/people/" + t + "/career_stats"
    res['links'] = []
    if int(offset) - int(limit) >= 0:
        pre = {"previous": s + "?offset=" + str(offset - limit) + "&limit=" + str(limit)}
        res['links'].append(pre)
    cur = {"current": s + "?offset=" + str(offset) + "&limit=" + str(limit)}
    res['links'].append(cur)
    pos = {"next": s + "?offset=" + str(offset + limit) + "&limit=" + str(limit)}
    res['links'].append(pos)
    return res



def find_related(resource1, resource2, primary_key, query, fields, offset, limit):

    p = find_primary_key(resource1)
    xxx = primary_key.split("_")
    t = copy.copy(query)
    for i in range(len(p)):
        t[p[i]] = [xxx[i]]

    wc = template_to_where_clause(t)
    all_fields = "select COLUMN_NAME from information_schema.COLUMNS where table_name =" + "'" + resource2 + "'"
    res = run_q(all_fields, None, True)
    s = set()
    for k in res:
        s.add(k["COLUMN_NAME"])
    f = ""
    print(res)
    if fields is not None:
        f = fields[0]
    else:
        for k in s:
            f += k + ","
        print(f)
        f = f[0:len(f)-1]
    subquery = "(" + "select * from " + resource1 + " natural join " + resource2 + ") as k"
    q = "select " + f + " from " + subquery + " " + wc + " limit " + str(limit) + " offset " + str(offset)
    result = run_q(q, None, True)

    res = {}
    res['data'] = result
    s = "/api/" + resource1 + "/" + primary_key + "/" + resource2
    if query is not None:
        s += "?"
        for k, v in query.items():
            s += k + "=" + v[0] + "&"
        s = s[0:len(s) - 1]
    if fields is not None:
        if query is None:
            s += "?fields="
        else:
            s += '&fields='
        for l in fields:
            s += l + ","
        s = s[0:len(s) - 1]
    if query is None and fields is None:
        s += "?"
    else:
        s += "&"
    res['links'] = []
    if int(offset) - int(limit) >= 0:
        pre = {"previous": s + "offset=" + str(offset - limit) + "&limit=" + str(limit)}
        res['links'].append(pre)
    cur = {"current": s + "offset=" + str(offset) + "&limit=" + str(limit)}
    res['links'].append(cur)
    pos = {"next": s + "offset=" + str(offset + limit) + "&limit=" + str(limit)}
    res['links'].append(pos)
    return res


def insert_related(resource, primary_key, related_resource, body):
    try:
        path_table = load_join_columns()
        primary_key = primary_key.split("_")
        kcs = find_primary_key(resource)
        kt = dict(zip(kcs, primary_key))
        path = path_table[resource+"_"+related_resource]
        tmp={}
        for e in path:
            v=kt[e[0]]
            tmp[e[1]]=v
        new_body={**tmp, **body}
        result = insert(related_resource, new_body)
        return result
    except pymysql.err.IntegrityError:
        print("Error")


def find_teammates(t):

    q = "select distinct p.playerID, p.nameLast, p.nameFirst, concat(b.teamID,'_',b.yearID) as team_year from \
people as p join batting as b on p.playerID = b.playerID \
where  (b.teamID, b.yearID)  in \
(select distinct teamID, yearID \
from batting where playerID = '" + t + "')"
    r = run_q(q, None, True)
    result = []
    pointer, count = 0, 1
    for index in range(1, len(r)):
        if r[index-count]['playerID'] == r[index]['playerID']:
            r[index-count]['team_year'] += "," + r[index]['team_year']
            count += 1
        else:
            result.append(r[index-count])
            count = 1
    return result


def update_table(resource, primary_key, template):
    q = "UPDATE " + resource + " SET "
    s = ""
    for k in template:
        s += k + "=" + "'" + template[k] + "'" + ","
    if s != "":
        s = s[0:len(s)-1]
    p = find_primary_key(resource)
    v = primary_key.split("_")
    dic = {}
    for i in range(len(p)):
        dic[p[i]] = [v[i]]
    wc = template_to_where_clause(dic)
    q += s + " " + wc
    print(q)
    run_q(q, None, False)


def load_possible_paths():

    q = \
        """
        SELECT
            TABLE_NAME,COLUMN_NAME,CONSTRAINT_NAME, REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME,
            ORDINAL_POSITION, POSITION_IN_UNIQUE_CONSTRAINT
        FROM
            INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE
            constraint_schema='lahman2017raw'
        and REFERENCED_TABLE_NAME is not null;
        """

    result = run_q(q, None, True)
    return result


def load_join_columns():

    fks = load_possible_paths()
    paths = {}

    for fk in fks:
        t = fk['TABLE_NAME'].lower()
        rt = fk['REFERENCED_TABLE_NAME'].lower()
        cn= fk['COLUMN_NAME']
        rcn = fk['REFERENCED_COLUMN_NAME']

        p1 = t + "_" + rt
        p2 = rt + "_" + t

        keys = paths.get(p1, None)
        if keys == None:
            paths[p1] = [[cn, rcn]]
        else:
            paths[p1].append([cn, rcn])

        keys = paths.get(p2, None)
        if keys == None:
            paths[p2] = [[rcn, cn]]
        else:
            paths[p2].append([rcn, cn])

    return paths



