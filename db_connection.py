import sqlite3

def insert_sales_plan(id, plan):
    try:
        sqlite_connection = sqlite3.connect('db.sqlite')
        cursor = sqlite_connection.cursor()
        print("Подключено к SQLite")

        sqlite_insert_with_param = '''INSERT INTO sales_plan(id, plan)
                                    VALUES (?, ?);'''
    
        data_tuple = (id, plan)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()
        print("Переменные внесены")
    
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

# insert_sales_plan("2023-03", 2000000)