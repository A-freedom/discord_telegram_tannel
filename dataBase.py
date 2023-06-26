import os
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('chat_messages.db')
cursor = conn.cursor()

# Create the chat_messages table (if it doesn't exist)
cursor.execute('''CREATE TABLE IF NOT EXISTS chat_messages
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   message TEXT,
                   file_name TEXT)''')

# Function to insert a chat message with file into the database
def insert_chat_message(message, file_path=None):
    file_name = os.path.basename(file_path) if file_path else None
    cursor.execute("INSERT INTO chat_messages (message, file_name) VALUES (?, ?)", (message, file_name))
    conn.commit()

# Example usage: Insert a chat message with text and file
message_text = "Hello, this is a chat message with a file."
file_path = "path/to/file.txt"
insert_chat_message(message_text, file_path)

# Fetch all chat messages from the database
cursor.execute("SELECT * FROM chat_messages")
messages = cursor.fetchall()

# Iterate over the chat messages and print them
for message in messages:
    message_id, text, file_name = message
    print(f"Message ID: {message_id}\nText: {text}\nFile Name: {file_name}\n")

# Close the database connection
conn.close()
