from flask import Flask, request, jsonify
import mysql.connector
import traceback

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host='db',
        user='root',
        password='yourpassword',
        database='testdb'
    )

@app.route('/data', methods=['POST'])
def insert_data():
    try:
        content = request.get_json(force=True)
        if not content:
            return jsonify({'error': 'No JSON received'}), 400

        print("Received JSON:", content)
        message = content.get('message', 'default message')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS messages (id INT AUTO_INCREMENT PRIMARY KEY, msg TEXT)"
        )
        cursor.execute("INSERT INTO messages (msg) VALUES (%s)", (message,))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'status': 'success', 'message': message})

    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
        return jsonify({'error': str(e)}), 400


@app.route('/data', methods=['GET'])
def get_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM messages")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        # Return as list of dicts
        results = [{'id': row[0], 'message': row[1]} for row in rows]
        return jsonify(results)

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
