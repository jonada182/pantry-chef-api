from bson import ObjectId
from flask import Blueprint, abort, jsonify, request
from project.db import initDB, json_encoder, parse_object_ids

# Define the blueprint
userBp = Blueprint('user', __name__)

# User Groceries endpoints

@userBp.route('/user/<user_id>/groceries')
def get_user_groceries(user_id):
    try:
        dbClient = initDB()
        user_groceries = dbClient['user.groceries']
        items = user_groceries.find({'user_id': user_id})
        return json_encoder(list(items), True)
    except Exception as e:
        abort(500, e)

@userBp.route('/user/<user_id>/groceries/<grocery_item_id>', methods=['POST'])
def post_user_grocery_item(user_id, grocery_item_id):
    try:
        dbClient = initDB()
        items_collection = dbClient['groceries.items']
        user_groceries = dbClient['user.groceries']
        grocery_item = items_collection.find_one({'_id': ObjectId(grocery_item_id)})
        if grocery_item is None:
            abort(404, 'Grocery item not found')
        existing_item = user_groceries.find_one({'user_id': user_id, 'grocery_item_id': grocery_item_id})
        if existing_item is not None:
            abort(400, 'Grocery item has been selected already')
        
        result = user_groceries.insert_one({'user_id': user_id, 'grocery_item_id': grocery_item_id})
        if result is None:
            abort(500, 'Selected item was not saved')
        
        return jsonify({'message': 'User grocery item has been saved'})
    except Exception as e:
        abort(500, e)

@userBp.route('/user/<user_id>/groceries/<grocery_item_id>', methods=['DELETE'])
def delete_user_grocery_item(user_id, grocery_item_id):
    try:
        dbClient = initDB()
        user_groceries = dbClient['user.groceries']
        
        result = user_groceries.delete_one({'user_id': user_id, 'grocery_item_id': grocery_item_id})
        if result.deleted_count <= 0:
            abort(500, 'User grocery item was not deleted')
        
        return jsonify({'message': 'User grocery item has been deleted'})
    except Exception as e:
        abort(500, e)

# User Recipes endpoints

@userBp.route('/user/<user_id>/recipes')
def get_user_recipes(user_id):
    try:
        dbClient = initDB()
        user_recipes = dbClient['user.recipes']
        items = user_recipes.find({'user_id': user_id})
        return json_encoder(list(items), True)
    except Exception as e:
        abort(500, e)

@userBp.route('/user/<user_id>/recipes', methods=['POST'])
def post_user_recipe(user_id):

    if not request.json or not 'title' in request.json:
        abort(400, 'Missing title parameter')

    if not request.json or not 'ingredients' in request.json:
        abort(400, 'Missing ingredients parameter')

    if not request.json or not 'instructions' in request.json:
        abort(400, 'Missing instructions parameter')

    recipe_title = request.json['title']
    recipe_ingredients = request.json['ingredients']
    recipe_instructions = request.json['instructions']
    recipe_image_url = None

    if 'image_url' in request.json:
        recipe_image_url = request.json['image_url']
    
    new_recipe = {
        'user_id': user_id,
        'title': recipe_title,
        'ingredients': recipe_ingredients,
        'instructions': recipe_instructions,
        'image_url': recipe_image_url
    }

    dbClient = initDB()
    user_recipes = dbClient['user.recipes']
    existing_recipe = user_recipes.find_one({'user_id': user_id, 'title': recipe_title})
    if existing_recipe is not None:
        abort(400, 'User recipe exists already')

    try:
        
        result = user_recipes.insert_one(new_recipe)
        if result is None:
            abort(500, 'User recipe was not saved')
        
        new_recipe['_id'] = str(result.inserted_id)
        
        return jsonify({'message': 'User recipe has been saved', 'data': new_recipe})
    except Exception as e:
        abort(500, e)

@userBp.route('/user/<user_id>/recipes/<recipe_id>', methods=['DELETE'])
def delete_user_recipe(user_id, recipe_id):
    try:
        dbClient = initDB()
        user_recipes = dbClient['user.recipes']
        
        result = user_recipes.delete_one({'user_id': user_id, '_id': ObjectId(recipe_id)})
        if result.deleted_count <= 0:
            abort(500, 'User recipe was not deleted')
        
        return jsonify({'message': 'User recipe has been deleted'})
    except Exception as e:
        abort(500, e)