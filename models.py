import datetime

from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin   #get_id()  is_authenticated
from peewee import *

DATABASE= MySQLDatabase('taco',host="localhost", port=3306)


class User(UserMixin, Model):  # have more than one parant class, UserMixin should be at the frount
    email = CharField(unique=True)
    password = CharField(max_length=100)
    is_admin = BooleanField(default=False)
    
    class Meta:
        database = DATABASE
        
    def get_tacos(self):
        return Taco.select().where(Taco.user == self)
    
    

    @classmethod  #cls refer to the class it belongs to
    def create_user(cls, email, password, admin=False):
        try:
            with DATABASE.transaction():
                cls.create(
                    email=email,
                    password=generate_password_hash(password), #nver hold the real password
                    is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists")

#Tacos have a protein, a shell, a true/false for cheese, and a freeform area for extras
class Taco(Model):
    protein = CharField(max_length=100)
    shell = CharField(max_length=100)
    cheese = BooleanField()
    user = ForeignKeyField(
        rel_model=User,   #the model the foreighkey points to 
        related_name='tacos'   #what the related model would call this model
    )
    extras = TextField()
    
    class Meta:
        database = DATABASE
       


        
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User,Taco], safe=True)
    DATABASE.close()       