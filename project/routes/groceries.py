import html
from bson import ObjectId
from flask import Blueprint, jsonify
from project.db import initDB, json_encoder, parse_object_ids

# Define the blueprint
groceriesBp = Blueprint('groceries', __name__)

# Define "groceries/categories" endpoint
@groceriesBp.route('/groceries/categories')
def get_categories():
    dbClient = initDB()
    categories_collection = dbClient['groceries.categories']
    categories = categories_collection.find()
    items = list(categories)
    return json_encoder(items, True)

# Define "groceries/categories/$id" endpoint
@groceriesBp.route('/groceries/categories/<category_id>')
def get_category(category_id):
    category_id = html.escape(category_id)
    dbClient = initDB()
    categories_collection = dbClient['groceries.categories']
    items_collection = dbClient['groceries.items']
    category = categories_collection.find_one({'_id': ObjectId(category_id)})
    if category:
        items = items_collection.find({'categoryId': category['_id']})
        parsed_items = parse_object_ids(list(items))
        category['items'] = parsed_items
        return json_encoder(category, True)
    else:
        return jsonify({'error': 'Category not found'})

# Define "groceries" endpoint
@groceriesBp.route('/groceries')
def get_groceries():
    dbClient = initDB()
    categories_collection = dbClient['groceries.categories']
    items_collection = dbClient['groceries.items']
    categories = categories_collection.find()
    result = []
    for category in categories:
        items = items_collection.find({'categoryId': category['_id']})
        parsed_items = parse_object_ids(list(items))
        category['items'] = parsed_items
        result.append(category)
    return json_encoder(result, True)