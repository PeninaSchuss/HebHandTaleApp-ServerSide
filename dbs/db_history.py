import os
import sqlite3
from config import DIR_PATH


def create_history_table():
    """
    This function creates the history table in the database
    :return: None
    """
    database_filename = "history.db"
    database_path = os.path.join(DIR_PATH, "dbs", database_filename)
    # Connect to the database
    connection = sqlite3.connect(database_path)

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
    """
    This function prints the history table
    :return: None
    """
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
    """
    This function adds a translation to the history table
    :param user: the user that requested the translation
    :param language_name: the language name
    :param word_to_translate: the word to translate
    :param translation: the translation
    :return: None
    """
    database_filename = "history.db"
    database_path = os.path.join(DIR_PATH, "dbs", database_filename)
    if not os.path.exists(database_path):
        create_history_table()
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute('''
           INSERT INTO history (user, language, word, translation)
           VALUES (?, ?, ?, ?)
       ''', (user, language_name, word_to_translate, translation))

    connection.commit()
    connection.close()


def get_history(user_token):
    """
    This function returns the history of a user
    :param user_token: the user token to retrieve the history for
    :return: history_list - the history of the user
    """
    database_filename = "history.db"
    database_path = os.path.join(DIR_PATH, "dbs", database_filename)
    if not os.path.exists(database_path):
        create_history_table()
    connection = sqlite3.connect(database_path)
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
