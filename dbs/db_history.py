import sqlite3


def create_history_table():
    connection = sqlite3.connect('history.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS translations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            language TEXT,
            word TEXT,
            translation TEXT
        )
    ''')

    connection.commit()
    connection.close()


def print_history_table():
    connection = sqlite3.connect('history.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM translations')
    rows = cursor.fetchall()

    print("Translation History:")
    for row in rows:
        print(f"ID: {row[0]}, User: {row[1]}, Language: {row[2]}, Word: {row[3]}, Translation: {row[4]}")

    connection.close()


if __name__ == '__main__':
    create_history_table()
    print_history_table()
