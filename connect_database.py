import sqlite3
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def SQLrequest(p, name=None, price=None, category_id=None, category=None):
    if p == '1':
        return cursor.execute("""
            SELECT products.name, products.price, categories.name 
            FROM products 
            JOIN categories ON products.category_id = categories.id
        """)
    if p == '2':
        return cursor.execute("SELECT name FROM categories")
    if p == '3':
        cursor.execute("INSERT INTO products(name, price, category_id) VALUES(?,?,?)", (name, price, category_id))
        return cursor.execute("SELECT * FROM products")  # Возвращаем всю таблицу после добавления
    if p == '4':
        cursor.execute("INSERT INTO categories(name) VALUES(?)", (category,))
        return cursor.execute("SELECT * FROM categories")
    if p == '5':
        cursor.execute("DELETE FROM products WHERE name = ?", (name,)) 
        return cursor.execute("SELECT * FROM products")  # Возвращаем всю таблицу после удаления

def print_menu():
    print('\n' + '-' * 60)
    print("Меню:")
    print('-' * 60)
    print("1. Вывести все товары")
    print("2. Вывести список доступных категорий")
    print("3. Добавить товар")
    print("4. Добавить категорию")
    print("5. Удалить товар")
    print("6. ВЫХОД")

def print_tables(p, table):
    if p == '1':
        print("\nСписок всех товаров:")
        print('-' * 51)
        print(f"|{'Название':<20}| {'Цена':<10}| {'Категория':<15}|")
        print('-' * 51)
        for element in table:
            print(f"|{element[0]:<20}| {element[1]:<10}| {element[2]:<15}|")
    elif p == '2':
        print("\nСписок доступных категорий:")
        print('-' * 32)
        print(f"|{'Категория':<30}|")
        print('-' * 32)
        for element in table:
            print(f"|{element[0]:<30}|")
    elif p == '3' or p == '5':
        print("\nТаблица товаров:")
        print('-' * 60)
        print(f"|{'ID':<5}| {'Название':<20}| {'Цена':<10}| {'ID категории':<15}|")
        print('-' * 60)
        cursor.execute("SELECT * FROM products")
        for product in cursor.fetchall():
            print(f"|{product[0]:<5}| {product[1]:<20}| {product[2]:<10}| {product[3]:<15}|")
    elif p == '4':
        print('-' * 49)
        print(f"|{'ID категории':<15}| {'Категории товаров':<30}|")
        print('-' * 49)
        for element in table:
            print(f"|{element[0]:<15}| {element[1]:<30}|")

def wait_for_enter():
    input("\nНажмите любую клавишу, чтобы продолжить...")

with sqlite3.connect("t1.db", timeout=20) as conn:
    cursor = conn.cursor()
    while True:
        clear_screen()
        print_menu()
        choice = input("Ваш выбор: ")
        
        if choice == '6':
            print("Выход из программы...")
            break

        if choice == '1':
            tables = SQLrequest(choice)
            print_tables(choice, tables.fetchall())  # Выводим всю таблицу товаров
            wait_for_enter()
        
        elif choice == '2':
            table = SQLrequest(choice)
            print_tables(choice, table.fetchall())  # Выводим таблицу из категорий
            wait_for_enter()
        
        elif choice == '3':
            name = input("Введите название товара: ")
            price = int(input("Введите стоимость товара: "))
            cursor.execute("SELECT id FROM categories")
            id_cat = [el[0] for el in cursor.fetchall()]
            table = cursor.execute("SELECT * FROM categories")
            print_tables('4', table.fetchall())
            category_id = (input("Введите ID категории из списка: "))
            while category_id == '' or category_id.isspace():
                category_id = (input("ID имеет неверный формат, введите корректный ID: "))
            while int(category_id) not in id_cat:
                category_id = int(input("Данной категории нет, введите существующую категорию: "))
            SQLrequest(choice, name, price, category_id)  # Добавление товара
            print("\nТовар добавлен!")
            table = SQLrequest('1')
            print_tables('1', table.fetchall())  # Выводим всю таблицу товаров после добавления
            wait_for_enter()
        
        elif choice == '4':
            category = input("Введите новую категорию: ")
            cursor.execute("SELECT name FROM categories")
            existing_categories = [el[0] for el in cursor.fetchall()]
            while category in existing_categories:
                category = input("Данная категория занята, введите новую категорию: ")
            SQLrequest(choice, category=category)  # Добавление категории
            print("Категория добавлена!")
            table = SQLrequest('2')  # Получаем обновленный список категорий
            print_tables('2', table.fetchall())  # Выводим таблицу категорий
            wait_for_enter()
        
        elif choice == '5':
            print("\nСписок всех товаров:")
            products = [el[0] for el in SQLrequest('1').fetchall()]
            print(", ".join(products))
            product = input("Введите товар, который хотите удалить: ")
            while product not in products:
                product = input("Товара нет в таблице, введите корректное название: ")
            SQLrequest(choice, product)  # Удаление товара
            print("\nТовар удалён.")
            table = SQLrequest('1')  # Получаем обновленный список товаров
            print_tables('1', table.fetchall())  # Выводим всю таблицу товаров после удаления
            wait_for_enter()
        
        else:
            print("Некорректный выбор. Пожалуйста попробуйте снова")
            wait_for_enter()
    cursor.close()
    conn.commit()