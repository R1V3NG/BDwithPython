from models import *
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
def print_menu():
    clear_screen()
    print('\n' + '-' * 60)
    print("Меню книжного магазина:")
    print('-' * 60)
    print("1. Вывести список всех книг")
    print("2. Вывести список жанров")
    print("3. Добавить новую книгу")
    print("4. Добавить новый жанр")
    print("5. Удалить книгу")
    print("6. Вывести список авторов")
    print("7. Сохранить изменения и выйти")
def print_books():
    clear_screen()
    print("\nСписок всех книг:")
    print('-' * 141)
    print(f"|{'ID':<5}|{'Название':<45}|{'Автор':<25}|{'Цена':<10}|{'Жанры':<50}|")
    print('-' * 141)
    
    for book in Book.select():
        genres = ", ".join([bg.genre.name for bg in book.genres])
        print(f"|{book.id:<5}|{book.title:<45}|{book.author.name:<25}|{book.price:<10}|{genres:<50}|")
    print('-' * 141)
def print_authors():
    print("\nСписок авторов в базе:")
    print('-' * 38)
    print(f"|{'ID':<5}|{'Автор':<30}|")
    print('-' * 38)
    for author in Author.select():
        print(f"|{author.id:<5}|{author.name:<30}|")
    print('-' * 38)
def print_genres():
    clear_screen()
    print("\nСписок жанров:")
    print('-' * 33)
    print(f"|{'ID':<5}|{'Жанр':<25}|")
    print('-' * 33)
    
    for genre in Genre.select():
        print(f"|{genre.id:<5}|{genre.name:<25}|")
    print('-' * 33)

def add_book():
    clear_screen()
    print("Добавление новой книги:")
    print_authors()
    
    title = input("\nВведите название книги: ")
    author_name = input("Введите имя автора: ").strip()
    price = input("Введите цену книги: ")
    
    try:
        # Получаем или создаем автора
        author, created = Author.get_or_create(name=author_name)
        if created:
            print(f"\nАвтор '{author_name}' добавлен в базу.")
        
        # Создаем книгу
        book = Book.create(title=title, author=author, price=price)
        
        # Добавляем жанры
        print_genres()
        genre_ids = input("Введите ID жанров через запятую (если не нужны, оставьте пустым): ").strip()
        
        if genre_ids:
            for genre_id in genre_ids.split(','):
                try:
                    genre = Genre.get_by_id(genre_id.strip())
                    BookGenre.create(book=book, genre=genre)
                except (DoesNotExist, ValueError):
                    print(f"Ошибка: жанр с ID {genre_id} не существует, пропускаем.")
        
        print(f"\nКнига '{title}' успешно добавлена!")
    except Exception as e:
        print(f"\nОшибка при добавлении книги: {e}")

def add_genre():
    clear_screen()
    print_genres()
    existing_genres = [g.name.lower() for g in Genre.select()]

    while True:
        name = input("\nВведите название нового жанра (или 'отмена' для выхода): ").strip()

        if name.lower() == 'отмена':
            return
        
        if not name or name.isspace():
            print("Название жанра не может быть пустым или содержать пробелы!")
            continue
            
        if name.lower() in existing_genres:
            print("Такой жанр уже существует!")
        else:
            break
    
    try:
        Genre.create(name=name)
        print(f"\nЖанр '{name}' успешно добавлен!")
    except Exception as e:
        print(f"\nОшибка при добавлении жанра: {e}")

def delete_book():
    clear_screen()
    print_books()
    
    try:
        book_id = input("\nВведите ID книги для удаления: ")
        if not book_id:
            print("ID книги не может быть пустым!")
            return
            
        book = Book.get_by_id(book_id)
        author = book.author
        title = book.title
        
        # Удаляем связи книги с жанрами
        BookGenre.delete().where(BookGenre.book == book).execute()
        
        # Удаляем саму книгу
        book.delete_instance()
        
        # Проверяем, есть ли у автора другие книги
        if not Book.select().where(Book.author == author).exists():
            author.delete_instance()
            print(f"\nКнига '{title}' успешно удалена!")
        else:
            print(f"\nКнига '{title}' успешно удалена!")
    except DoesNotExist:
        print("\nКнига с таким ID не найдена!")
    except Exception as e:
        print(f"\nОшибка при удалении книги: {e}")

def wait_for_enter():
    input("\nНажмите Enter чтобы продолжить...")

def main():
    db.connect()
    
    while True:
        print_menu()
        choice = input("\nВаш выбор: ")
        
        if choice == '1':
            print_books()
            wait_for_enter()
        elif choice == '2':
            print_genres()
            wait_for_enter()
        elif choice == '3':
            add_book()
            wait_for_enter()
        elif choice == '4':
            add_genre()
            wait_for_enter()
        elif choice == '5':
            delete_book()
            wait_for_enter()
        elif choice == '6':
            clear_screen()
            print_authors()
            wait_for_enter()
        elif choice == '7':
            try:
                db.commit()
                print("\nВсе изменения успешно сохранены в базе данных!")
                break
            except Exception as e:
                print(f"\nОшибка при сохранении изменений: {e}")
                wait_for_enter()
        else:
            print("\nНекорректный выбор!")
            wait_for_enter()
    
    db.close()

if __name__ == '__main__':
    main()