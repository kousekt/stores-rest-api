import sqlite3
from models_pkg.user import UserModel
from flask_restful import Resource, reqparse


class UserRegister(Resource):
  parser = reqparse.RequestParser()
  # It's only going to have these
  parser.add_argument('username',                      
                      required=True, 
                      type=str,
                      help="This field cannot be left blank"
                      )
  parser.add_argument('password',                      
                      required=True, 
                      type=str,
                      help="This field cannot be left blank"
                      )


  def post(self):
    data = UserRegister.parser.parse_args()
    if UserModel.find_by_username(data['username']):
       return {"message": "User already exists"}, 400

    # You need these 2 ** instead of 1 for the unpacking
    user = UserModel(**data)
    user.save_to_db()
    
    return {"message":"User Created"}, 201
