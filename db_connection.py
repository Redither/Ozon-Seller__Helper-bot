import sqlite3

try:
    sqlite_connection = sqlite3.connect('db.sqlite')
    sqlite_create_table_query = '''CREATE TABLE sales_plan (
                                    id TEXT PRIMARY KEY,
                                    plan INTEGER NOT NULL
                                );'''
    
    cursor = sqlite_connection.cursor()
    print("База данных создана и успешно подключена к SQLite")
    cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()
    print("Таблица создана")
    
    cursor.close()

except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
finally:
    if (sqlite_connection):
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")