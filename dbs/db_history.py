import os
import sqlite3
from datetime import datetime

def create_history_table():
    connection = sqlite3.connect('history.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            language TEXT,
            word TEXT,
            translation TEXT,
            insertion_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    connection.commit()
    connection.close()

def print_history_table():
    connection = sqlite3.connect('history.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM history')
    rows = cursor.fetchall()

    print("Translation History:")
    for row in rows:
        print(
            f"ID: {row[0]}, User: {row[1]}, Language: {row[2]}, Word: {row[3]}, Translation: {row[4]}, Insertion Date: {row[5]}")

    connection.close()

def add_history_to_db(user, language_name, word_to_translate, translation):
    db_path = os.path.join(os.path.dirname(__file__), 'history.db')
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
           INSERT INTO history (user, language, word, translation)
           VALUES (?, ?, ?, ?)
       ''', (user, language_name, word_to_translate, translation))

    connection.commit()
    connection.close()

def get_history(user_token):
    db_path = os.path.join(os.path.dirname(__file__), 'history.db')
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
        SELECT * FROM history WHERE user = ? ORDER BY insertion_date DESC
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
            "translation": row[4],
            "insertion_date": row[5]
        })

    return history_list

if __name__ == '__main__':
    create_history_table()
    print_history_table()

    # Add a block to retrieve and print history by user
    user_token_to_retrieve = "@Penina"
    user_history = get_history(user_token_to_retrieve)
    print("\nUser History:")
    for entry in user_history:
        print(entry)
