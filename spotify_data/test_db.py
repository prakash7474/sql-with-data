import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='P@ssw0rd',
        database='spotify_db'
    )
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM tracks')
    count = cursor.fetchone()[0]
    print(f'Tracks count: {count}')
    cursor.execute('SHOW TABLES')
    tables = cursor.fetchall()
    print(f'Tables: {tables}')
    conn.close()
    print("Database test successful!")
except Exception as e:
    print(f'Error: {e}')
