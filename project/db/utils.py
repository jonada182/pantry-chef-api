import json
from bson import json_util, ObjectId
from flask import jsonify

# Helper to manage json encoding, parsing ObjectIds if required
def json_encoder(items, parse_ids = False):
    if parse_ids:
        items = parse_object_ids(items)
    data = json.loads(json_util.dumps(items))
    return jsonify(data)

# From an array of objects, convert fields of type ObjectId to String
def parse_object_ids(items):
    if type(items) is dict:
        items['_id'] = str(items['_id'])
    for item in items:
        if type(item) is dict:
            for key, value in item.items():
                if isinstance(value, ObjectId):
                    item[key] = str(value)
    return items