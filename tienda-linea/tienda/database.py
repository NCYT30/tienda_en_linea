from peewee import *
from datetime import datetime


database = MySQLDatabase('tienda_en_linea',
                         user = 'root',
                         password = 'NCYT30',
                         host = 'localhost',
                         port = 3306)

class User(Model):
    username = CharField()
    email = CharField()

    class Meta:
        database = database
        table_name = 'User'


class Product(Model):
    name = CharField()
    description = TextField()
    price = DecimalField(max_digits=10, decimal_places=2)
    stock = IntegerField()

    class Meta:
        database = database
        table_name = 'Product'

class Address(Model):
    user = ForeignKeyField(User, backref='addresses')
    street = CharField()
    city = CharField()
    postal_code = CharField()

    class Meta:
        database = database
        table_name = 'Address'

class Review(Model):
    product_id = ForeignKeyField(Product, backref='reviews')
    user_id = ForeignKeyField(User, backref='reviews')
    rating = IntegerField()
    comment = TextField()

    class Meta:
        database = database
        table_name = 'Review'

class Category(Model):
    name = CharField()
    description = CharField()

    class Meta:
        database = database
        table_name = 'Category'

class ProductCategory(Model):
    product = ForeignKeyField(Product, backref='categories')
    category = ForeignKeyField(Category, backref='products')

    class Meta:
        database = database
        table_name = 'ProductCategory'