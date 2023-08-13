import sqlite3

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


# Query data
select_query = "SELECT data_string FROM popular_words;"
cursor.execute(select_query)

# Fetch all rows
rows = cursor.fetchall()

for row in rows:
    print(row[0])

# Close the connection
connection.close()
