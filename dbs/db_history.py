import os
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


def add_history_to_db(user, language_name, word_to_translate, translation):
    db_path = os.path.join(os.path.dirname(__file__), 'history.db')
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
           INSERT INTO translations (user, language, word, translation)
           VALUES (?, ?, ?, ?)
       ''', (user, language_name, word_to_translate, translation))

    connection.commit()
    connection.close()


def get_history(user_token):
    db_path = os.path.join(os.path.dirname(__file__), 'history.db')
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
        SELECT * FROM translations WHERE user = ?
    ''', (user_token,))

    rows = cursor.fetchall()
    connection.close()

    history_list = []
    for row in rows:
        history_list.append({
            "id": row[0],
            "user": row[1],
            "language": row[2],
            "word": row[3],
            "translation": row[4]
        })

    return history_list


if __name__ == '__main__':
    create_history_table()
    print_history_table()
