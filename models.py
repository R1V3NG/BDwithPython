from peewee import *

db = SqliteDatabase('BookSeller.db')

class BaseModel(Model):
    class Meta:
        database = db

class Author(BaseModel):
    name = CharField(unique=True)
    class Meta:
        database = db
        db_table = "authors" 

class Book(BaseModel):
    title = CharField()
    author = ForeignKeyField(Author, backref='books') 
    price = DecimalField(decimal_places=2)
    class Meta:
        database = db
        db_table = "books"

class Genre(BaseModel):
    name = CharField(unique=True)
    class Meta:
        database = db
        db_table = "genres"

class BookGenre(BaseModel):
    book = ForeignKeyField(Book, backref='genres')
    genre = ForeignKeyField(Genre, backref='books')
    class Meta:
        database = db
        db_table = "book_genres"

