import os
import sqlite3

from flask import jsonify


def create_popular_word_table():
    # Connect to the database
    connection = sqlite3.connect("popular_words.db")

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
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'popular_words.db')
        connection = sqlite3.connect(db_path)

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


if __name__ == '__main__':
    create_popular_word_table()
    print_popular_word_table()
