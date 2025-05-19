import mysql.connector
import time

# Retry logic in case DB isn't ready yet
for _ in range(10):
    try:
        conn = mysql.connector.connect(
            host='db',
            user='root',
            password='example',
            database='testdb'
        )
        break
    except mysql.connector.Error:
        print("Waiting for MySQL...")
        time.sleep(2)
else:
    print("Failed to connect to database.")
    exit(1)

cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INT AUTO_INCREMENT PRIMARY KEY,
        content TEXT
    )
""")

# Insert a message
cursor.execute("INSERT INTO messages (content) VALUES (%s)", ("Hello from Docker!",))
conn.commit()

# Fetch and print messages
cursor.execute("SELECT * FROM messages")
rows = cursor.fetchall()
for row in rows:
    print(f"Row: {row}")

conn.close()
