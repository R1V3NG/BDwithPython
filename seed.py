from models import *
TABLES = [Author, Book, Genre, BookGenre]
with db:
    db.drop_tables(TABLES)
    db.create_tables(TABLES)

     # Создаем авторов
    authors = [
        {'name': 'Джоан Роулинг'},
        {'name': 'Джордж Оруэлл'},
        {'name': 'Агата Кристи'}
    ]
    Author.insert_many(authors).execute()

    # Создаем жанры
    genres = [
        {'name': 'Фэнтези'},
        {'name': 'Антиутопия'},
        {'name': 'Детектив'},
        {'name': 'Приключения'}
    ]
    Genre.insert_many(genres).execute()

    # Создаем книги и связи
    books = [
        {
            'title': 'Гарри Поттер и философский камень',
            'author': 'Джоан Роулинг',
            'price': 599.99,
            'genres': ['Фэнтези', 'Приключения']
        },
        {
            'title': '1984',
            'author': 'Джордж Оруэлл',
            'price': 450.50,
            'genres': ['Антиутопия']
        },
        {
            'title': 'Убийство в Восточном экспрессе',
            'author': 'Агата Кристи',
            'price': 399.99,
            'genres': ['Детектив']
        }
    ]

    for book_data in books:
        author = Author.get(Author.name == book_data['author'])
        book = Book.create(
            title=book_data['title'],
            author=author,
            price=book_data['price']
        )
        
        # Добавляем связи с жанрами
        for genre_name in book_data['genres']:
            genre = Genre.get(Genre.name == genre_name)
            BookGenre.create(book=book, genre=genre)

    # c1 = Category.create(name = "Еда")
    # # c2 = Category(name = "Одежда")
    # c2 = Category()
    # c2.name = "Одежда"
    # c2.save()

#     p1 = Product.create(name ="Хлеб", price = 50, category_id = c1)
