# Lahman.py

# Convert to/from web native JSON and Python/RDB types.
import json

# Include Flask packages
from flask import Flask
from flask import request
import copy
import pymysql
import SimpleBO


# The main program that executes. This call creates an instance of a
# class and the constructor starts the runtime.
app = Flask(__name__)

def parse_and_print_args():

    fields = None
    in_args = None
    offset = 0
    limit = 10
    if request.args is not None:
        in_args = dict(copy.copy(request.args))
        fields = copy.copy(in_args.get('fields', None))
        if fields:
            del(in_args['fields'])
        if "offset" in in_args:
            offset = int(in_args["offset"][0])
            in_args.pop("offset")
        if "limit" in in_args:
            if int(in_args["limit"][0]) < 10:
                limit = int(in_args["limit"][0])
            in_args.pop("limit")
    try:
        if request.data:
            body = json.loads(request.data.decode('utf-8'))
        else:
            body = None
    except Exception as e:
        print("Got exception = ", e)
        body = None

    print("Request.args : ", json.dumps(in_args))
    return in_args, fields, body, offset, limit


@app.route('/api/<resource>', methods=['GET', 'POST'])
def get_resource(resource):
    in_args, fields, body, offset, limit = parse_and_print_args()
    print(parse_and_print_args())
    if request.method == 'GET':
        result = SimpleBO.find_by_template(resource, in_args, fields, offset, limit)
        return json.dumps(result, indent=2), 200, \
               {"content-type": "application/json; charset: utf-8"}
    elif request.method == 'POST':
        SimpleBO.insert(resource, body)
        return "Method " + request.method + " on resource " + resource + \
               " implemented!", 200, \
               {"content-type": "application/json; charset: utf-8"}
    else:
        return "Method " + request.method + " on resource " + resource + \
               " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}


@app.route('/api/<resource>/<primary_key>', methods=['GET', 'DELETE', 'PUT'])
def find_rows_by_primary_key(resource, primary_key):
    in_args, fields, body, offset, limit = parse_and_print_args()
    if request.method == 'GET':
        result = SimpleBO.find_by_primary_key(resource, primary_key, fields, offset, limit)
        return json.dumps(result, indent=2), 200, {"content-type": "application/json; charset: utf-8"}
    elif request.method == 'DELETE':
        SimpleBO.delete(resource, primary_key)
        return "Method " + request.method + " on resource " + resource + \
               " implemented!", 200, \
               {"content-type": "application/json; charset: utf-8"}
    elif request.method == 'PUT':
        SimpleBO.update_table(resource, primary_key, body)
        return "Method " + request.method + " on resource " + resource + \
               " implemented!", 200, \
               {"content-type": "application/json; charset: utf-8"}


@app.route('/api/roster', methods=['GET'])
def find_roster():
    in_args, fields, body, offset, limit = parse_and_print_args()
    result = SimpleBO.roster(in_args, offset, limit)
    return json.dumps(result, indent=2), 200, {"content-type": "application/json; charset: utf-8"}


@app.route('/api/people/<playerid>/career_stats', methods=['GET'])
def find_career_stas_playerid(playerid):
    in_args, fields, body, offset, limit = parse_and_print_args()
    result = SimpleBO.find_rows_by_career_stas_by_playerid(playerid, offset, limit)
    return json.dumps(result, indent=2), 200, {"content-type": "application/json; charset: utf-8"}


@app.route('/api/teammates/<playerid>', methods=['GET'])
def find_teammates(playerid):
    result = SimpleBO.find_teammates(playerid)
    return json.dumps(result, indent=2), 200, {"content-type": "application/json; charset: utf-8"}


@app.route('/api/<resource>/<primary_key>/<related_resource>', methods=['GET', 'POST'])
def related_query(resource, primary_key, related_resource):
    in_args, fields, body, offset, limit = parse_and_print_args()
    if request.method == 'GET':
        result = SimpleBO.find_related(resource, related_resource, primary_key, in_args, fields, offset, limit)
        return json.dumps(result, indent=2), 200, {"content-type": "application/json; charset: utf-8"}
    elif request.method == 'POST':
        SimpleBO.insert_related(resource, primary_key, related_resource, body)
        return "Method " + request.method + " on resource " + resource + \
               " implemented!", 200, \
               {"content-type": "application/json; charset: utf-8"}

if __name__ == '__main__':
    app.run()

