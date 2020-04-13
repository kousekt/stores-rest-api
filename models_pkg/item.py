from db import db

class ItemModel(db.Model):
  __tablename__ = 'items'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  price = db.Column(db.Float(precision=2))
  store_id = db.Column(db.Integer, db.ForeignKey('stores.id')) # points to store=>_id
  # We don't have to do a join, instead e do this..
  store = db.relationship('StoreModel') # Every item will now have a "store" which will match that store id

  def __init__(self, name, price, store_id):  # lesson 105, 10:10
    self.name = name
    self.price = price
    self.store_id = store_id

  def json(self):
    return {'name':self.name, 'price':self.price}

  @classmethod
  def find_by_name(cls, name):
    return cls.query.filter_by(name=name).first() # select * from items where name=? LIMIT 1
    
  def save_to_db(self): # Upsert
    db.session.add(self)
    db.session.commit()
 
  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit();
    

