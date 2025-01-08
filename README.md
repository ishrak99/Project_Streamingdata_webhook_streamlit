# Project_Streamingdata_webhook_streamlit
To store webhook data in a database, you can integrate a **database (e.g., SQLite, PostgreSQL, MySQL)** with your Flask backend. Below, I'll walk you through how to modify the Flask server to store webhook data in a SQLite database.

---

### Updated Flask Server with Database Integration

#### Full Code with Database

```python
from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database setup: Connect to SQLite and create a table
def init_db():
    conn = sqlite3.connect("webhook_data.db")
    cursor = conn.cursor()
    # Create a table to store webhook data
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS webhook_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT NOT NULL,
            order_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            received_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Insert data into the database
def store_webhook_data(event, order_id, amount):
    conn = sqlite3.connect("webhook_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO webhook_data (event, order_id, amount, received_at)
        VALUES (?, ?, ?, ?)
    """, (event, order_id, amount, datetime.now().isoformat()))
    conn.commit()
    conn.close()

# Flask route to handle webhook data
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        if data and "event" in data and "order_id" in data and "amount" in data:
            # Store the data in the database
            store_webhook_data(data["event"], data["order_id"], data["amount"])
            return jsonify({"message": "Data received and stored"}), 200
        else:
            return jsonify({"error": "Invalid data format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Route to retrieve data (optional, for debugging purposes)
@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        conn = sqlite3.connect("webhook_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM webhook_data")
        rows = cursor.fetchall()
        conn.close()

        # Convert data to JSON format
        data = [{"id": row[0], "event": row[1], "order_id": row[2], "amount": row[3], "received_at": row[4]} for row in rows]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Initialize the database
    init_db()
    # Run the Flask app
    app.run(host='0.0.0.0', port=5100)
```

---

### Explanation

#### 1. Database Setup

- **SQLite** is used for simplicity.
- A table `webhook_data` is created with the following schema:
  - `id`: Auto-incremented primary key.
  - `event`: Event name (e.g., `order_created`).
  - `order_id`: Unique order ID.
  - `amount`: Transaction amount.
  - `received_at`: Timestamp of when the data was received.

#### 2. Storing Data

- The `store_webhook_data` function inserts the webhook data into the `webhook_data` table.

#### 3. Endpoint `/webhook`

- When a POST request is sent to `/webhook`:
  1. The JSON payload is parsed.
  2. The `store_webhook_data` function is called to save the data in the database.
  3. A success response (`200`) is returned.

#### 4. Endpoint `/get_data` (Optional)

- This endpoint retrieves all stored webhook data from the database.
- Useful for debugging or verifying the data storage.

---

### Testing the Updated Flask Server

1. Start the Flask server:
   ```bash
   python webhook_server.py
   ```

2. Send POST requests to the `/webhook` endpoint:
   ```bash
   curl -X POST -H "Content-Type: application/json" \
   -d '{"event": "order_created", "order_id": 12345, "amount": 150.75}' \
   http://localhost:5100/webhook
   ```

3. Verify the data in the database by accessing the `/get_data` endpoint:
   ```bash
   curl -X GET http://localhost:5100/get_data
   ```

   Example Response:
   ```json
   [
       {
           "id": 1,
           "event": "order_created",
           "order_id": 12345,
           "amount": 150.75,
           "received_at": "2025-01-08T12:30:00.123456"
       }
   ]
   ```

---

### Querying the Database

To query the database manually, you can use the SQLite command-line tool or a database browser:

1. Open the database:
   ```bash
   sqlite3 webhook_data.db
   ```

2. Run SQL queries:
   ```sql
   SELECT * FROM webhook_data;
   ```

---

### Integration with Streamlit

To display the webhook data in a Streamlit app:

#### Streamlit Code:
```python
import streamlit as st
import requests
import pandas as pd

# Flask server URL
FLASK_URL = "http://localhost:5100"

# Fetch data from the Flask server
def fetch_data():
    try:
        response = requests.get(f"{FLASK_URL}/get_data")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching data: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {e}")
        return []

# Streamlit app
st.title("Webhook Data Viewer")

st.subheader("Stored Webhook Data")

data = fetch_data()
if data:
    df = pd.DataFrame(data)
    st.dataframe(df)
else:
    st.write("No data available.")
```

#### How It Works:
1. The Streamlit app fetches data from the `/get_data` endpoint of the Flask server.
2. The data is displayed in a table using `st.dataframe`.

---

### Testing End-to-End Workflow

1. Start the Flask server:
   ```bash
   python webhook_server.py
   ```

2. Start the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

3. Push webhook data using `curl` or a Python script:
   ```bash
   curl -X POST -H "Content-Type: application/json" \
   -d '{"event": "order_created", "order_id": 12345, "amount": 150.75}' \
   http://localhost:5100/webhook
   ```

4. Open the Streamlit app to view the data.

---

### Next Steps

1. **Switch to a Production Database**:
   - Use PostgreSQL, MySQL, or another robust database for production.
2. **Authentication**:
   - Secure the `/webhook` endpoint with an API key or token to prevent unauthorized access.
3. **Data Retention Policy**:
   - Implement a cleanup process to delete old data if the database grows too large.

Let me know if you need help with further enhancements! 🚀
