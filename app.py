from flask import Flask, jsonify, request, render_template
from flask_smorest import abort
from db import items, stores
import uuid

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/store', methods=['POST'])
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.route('/store/<string:store_id>')
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return abort(404, message="store not found")


@app.route('/store')
def get_stores():
    return {'stores': list(stores.values())}


@app.route('/item', methods=['POST'])
def create_item():
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        abort(404, message="item not found")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    return item, 201


@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}


@app.route('/item/<string:item_id>')
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="item not found")


if __name__ == '__main__':
    app.run(debug=True)
