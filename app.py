from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from secure import authenticate, identity
from resources_pkg.user import UserRegister
from resources_pkg.item import Item, ItemList
from resources_pkg.store import Store, StoreList
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///therondata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # lesson 105 10:10
app.secret_key = 'secretkey'
api = Api(app)

# Tell the alchemy to create the database so we don't need create_tables.py anymore
# This method before the first request to the app
# It only creates tables that it sees.  Has to go thru imports..  Looks at the models in the imports..
# You IMPORT the things you want SQLAlchemy to know about..
@app.before_first_request
def create_tables():
  db.create_all()  # Create the db in the SQLALCHEMY_DATABASE_URI

# That will use the authenticate and identity together  76, 1:00
# JWT creates a new endpoint #/auth
# auth first and then identity() function when it calsl the next function...
jwt = JWT(app, authenticate, identity)  #/auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':  # run this ONLY if you do python app.py, not if you're doing import
  db.init_app(app)
  app.run(port=5000, debug=True)
