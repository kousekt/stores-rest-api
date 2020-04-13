from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models_pkg.item import ItemModel

class Item(Resource):
  # Parser looks in the json payload
  parser = reqparse.RequestParser()
  parser.add_argument('price',
    type=float,
    required=True,  # All requests need to have a price
    help="This field cannot be left blank"
  )
  parser.add_argument('store_id',
    type=int,
    required=True,  # All requests need to have a price
    help="Every item needs a store id"
  )

  # We need to authenticate before we can call this..
  @jwt_required() 
  def get(self, name):
    item = ItemModel.find_by_name(name)
    if item:
      return item.json()  
    return {'message':'Item not found'}    

  @jwt_required()  # for production
  def post(self, name):
    if ItemModel.find_by_name(name):    
      return {'message': f"An item with {name} already exists"}, 400

    data = Item.parser.parse_args()
    item = ItemModel(name, **data) # Lesson 110 12:15

    try:
      item.save_to_db()
    except:
      return {"message":"An error occured with inserting.."}, 500 # Internal server error
    
    return item.json(), 201

  @jwt_required()  # for production
  def put(self, name):
    data = Item.parser.parse_args()
    item = ItemModel.find_by_name(name)      
        
    if item is None:
      item = ItemModel(name, **data)
    else:
      item.price = data['price']
      item.price = data['store_id']

    item.save_to_db()
    return item.json()

  @jwt_required()  
  def delete(self, name):
    item = ItemModel.find_by_name(name)
    if item:
      item.delete_from_db()
    return {'message': 'Item Deleted'}

class ItemList(Resource):
  @jwt_required()  # for production 
  def get(self):
    return {'items': [item.json() for item in ItemModel.query.all()]}  
    # with lambda  lesson - 108  4:15
    # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}    
