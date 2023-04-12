import json

def seedData (dbClient):
    if dbClient is None:
        return
    db = dbClient
    # Save grocery categories into MongoDB
    categories_collection_name = 'groceries.categories'
    items_collection_name = 'groceries.items'
    if categories_collection_name in db.list_collection_names():
        print(f'The collection {categories_collection_name} already exists')
    else:
        print(f'The collection {categories_collection_name} does not exist')
        with open('project/data/groceries-categories.json') as f:
            data = json.load(f)
        collection = db[categories_collection_name]
        collection.insert_many(data)
        print(f'The data has been imported into the {categories_collection_name} collection')

    # Load categories from JSON file
    with open('project/data/groceries-items.json') as f:
        categories = json.load(f)

    # Get categories collection
    categories_collection = db[categories_collection_name]

    # Get items collection
    items_collection = db[items_collection_name]


    if items_collection_name in db.list_collection_names():
        print(f'The collection {items_collection_name} already exists')
    else:
        print(f'The collection {items_collection_name} does not exist')
        # Process each category
        items = []
        for category in categories:
            # Find category ID from MongoDB
            category_doc = categories_collection.find_one({'name': category['name']})
            if category_doc:
                category_id = category_doc['_id']
            else:
                print(f"Category '{category['name']}' not found in database")
                continue

            # Add items to list
            for item_name in category['items']:
                item = {
                    'name': item_name,
                    'categoryId': category_id,
                    'slug': item_name.lower().replace(' ', '-'),
                    'id': f"{category_id}-{item_name.lower().replace(' ', '-')}"
                }
                items.append(item)

        # Save items to MongoDB
        if items:
            result = items_collection.insert_many(items)
            print(f"Inserted {len(result.inserted_ids)} items into the {items_collection.name} collection")
        else:
            print("No items to insert")

        print("Items saved to MongoDB")
