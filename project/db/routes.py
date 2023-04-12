# Get categories collection
import json
from flask import jsonify
from project.db import dbClient
from project import app
from bson import json_util, ObjectId

categories_collection = dbClient['groceries.categories']

# Get items collection
items_collection = dbClient['groceries.items']

# Define "groceries/categories" endpoint
@app.route('/groceries/categories')
def get_categories():
    categories = categories_collection.find()
    items = list(categories)
    return json_encoder(items, True)

# Define "groceries/categories/$id" endpoint
@app.route('/groceries/categories/<category_id>')
def get_category(category_id):
    category = categories_collection.find_one({'_id': ObjectId(category_id)})
    if category:
        items = items_collection.find({'categoryId': category['_id']})
        parsed_items = parse_object_ids(list(items))
        category['items'] = parsed_items
        return json_encoder(category, True)
    else:
        return jsonify({'error': 'Category not found'})

# Define "groceries" endpoint
@app.route('/groceries')
def get_groceries():
    categories = categories_collection.find()
    result = []
    for category in categories:
        items = items_collection.find({'categoryId': category['_id']})
        parsed_items = parse_object_ids(list(items))
        category['items'] = parsed_items
        result.append(category)
    return json_encoder(result, True)

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