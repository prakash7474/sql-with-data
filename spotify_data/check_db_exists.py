import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='P@ssw0rd'
    )
    cursor = conn.cursor()
    cursor.execute('SHOW DATABASES')
    databases = cursor.fetchall()
    print(f'Databases: {[db[0] for db in databases]}')
    if ('spotify_db',) in databases:
        print("spotify_db exists")
        cursor.execute('USE spotify_db')
        cursor.execute('SHOW TABLES')
        tables = cursor.fetchall()
        print(f'Tables in spotify_db: {[t[0] for t in tables]}')
        if tables:
            cursor.execute('SELECT COUNT(*) FROM tracks')
            count = cursor.fetchone()[0]
            print(f'Tracks count: {count}')
        else:
            print("No tables found in spotify_db")
    else:
        print("spotify_db does not exist")
    conn.close()
except Exception as e:
    print(f'Error: {e}')
