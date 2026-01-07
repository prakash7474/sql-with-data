import mysql.connector

# Check port 3306
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
    print(f'Port 3306 - Tracks count: {count}')
    conn.close()
except Exception as e:
    print(f'Port 3306 error: {e}')

# Check port 3308
try:
    conn = mysql.connector.connect(
        host='localhost',
        port=3308,
        user='root',
        password='P@ssw0rd',
        database='spotify_db'
    )
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM tracks')
    count = cursor.fetchone()[0]
    print(f'Port 3308 - Tracks count: {count}')
    conn.close()
except Exception as e:
    print(f'Port 3308 error: {e}')
