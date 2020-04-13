from models_pkg.user import UserModel
from werkzeug.security import safe_str_cmp

def authenticate(username, password):
  #print(f"In authenticate {username} - {password}")
  # None is default value if we cannot find it.  
  user = UserModel.find_by_username(username)
  if user is None:
    print("Cannot find user")  
  if user and safe_str_cmp(user.password,password):
    return user

def identity(payload):
  user_id = payload['identity']
  #print(f"userid {user_id} ")
  return UserModel.find_by_id(user_id)
