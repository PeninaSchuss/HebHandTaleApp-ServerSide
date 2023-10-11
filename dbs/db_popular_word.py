import os
import sqlite3
from flask import jsonify
from config import DIR_PATH


def create_popular_word_table():
    """
    This function creates the popular_words table
    :return: None
    """
    database_filename = "popular_words.db"
    database_path = os.path.join(DIR_PATH, "dbs", database_filename)
    # Connect to the database
    connection = sqlite3.connect(database_path)

    # Create a cursor
    cursor = connection.cursor()

    # Check if the table exists
    check_table_query = '''
    SELECT name FROM sqlite_master WHERE type='table' AND name='popular_words';
    '''

    cursor.execute(check_table_query)
    table_exists = cursor.fetchone()

    if not table_exists:
        # Create the table
        create_table_query = '''
        CREATE TABLE popular_words (
            data_string TEXT
        );
        '''

        cursor.execute(create_table_query)

        # Commit the table creation
        connection.commit()
        connection.close()


def print_popular_word_table():
    """
    This function prints the popular_words table content
    :return: None
    """
    # Connect to the database
    connection = sqlite3.connect("popular_words.db")

    # Create a cursor
    cursor = connection.cursor()
    # Query data
    select_query = "SELECT data_string FROM popular_words;"
    cursor.execute(select_query)

    # Fetch all rows
    rows = cursor.fetchall()

    for row in rows:
        print(row[0])

    # Close the connection
    connection.close()


def add_word_to_db(word_to_add):
    """
    This function adds a word to the popular_words table
    :param word_to_add: the word to add
    :return: None
    """
    database_filename = "popular_words.db"
    database_path = os.path.join(DIR_PATH, "dbs", database_filename)
    if not os.path.exists(database_path):
        create_popular_word_table()
    try:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        # Check if the word already exists in the table
        select_query = '''
        SELECT data_string FROM popular_words WHERE data_string = ?;
        '''
        cursor.execute(select_query, (word_to_add,))
        existing_word = cursor.fetchone()

        if existing_word:
            return jsonify({"message": f"Word '{word_to_add}' already exists in popular_words.db"}), 200  # OK

        # Insert the word into the table
        insert_query = '''
        INSERT INTO popular_words (data_string)
        VALUES (?);
        '''
        cursor.execute(insert_query, (word_to_add,))
        connection.commit()
        connection.close()
        return jsonify({"message": f"Word '{word_to_add}' added to popular_words.db"}), 201  # Created

    except Exception as e:
        connection.close()
        return jsonify({"error": str(e)}), 500  # Internal Server Error


def get_all_popular_words():
    """
    This function returns all the popular words from the database
    :return: popular_words - a set of all the popular words in the database
    """
    database_filename = "popular_words.db"
    database_path = os.path.join(DIR_PATH, "dbs", database_filename)
    if not os.path.exists(database_path):
        create_popular_word_table()
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    # Fetch popular words from the database
    cursor.execute("SELECT data_string FROM popular_words;")
    popular_words = set(row[0] for row in cursor.fetchall())
    connection.close()
    return popular_words


if __name__ == '__main__':
    create_popular_word_table()
    print_popular_word_table()
