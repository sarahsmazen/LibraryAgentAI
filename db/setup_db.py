import sqlite3
import os

# Define the paths for the database and SQL files 
DB_PATH = os.path.join(os.path.dirname(__file__), 'library.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')
SEED_PATH = os.path.join(os.path.dirname(__file__), 'seed.sql')

def setup_database():
    """Creates the database and populates it with initial data."""
    try:
        # Connect to SQLite (it will create the file if it doesn't exist) [cite: 6]
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Read and execute schema.sql [cite: 46]
        print(f"Applying schema from {SCHEMA_PATH}...")
        with open(SCHEMA_PATH, 'r') as f:
            cursor.executescript(f.read())

        # Read and execute seed.sql [cite: 46, 51]
        print(f"Seeding data from {SEED_PATH}...")
        with open(SEED_PATH, 'r') as f:
            cursor.executescript(f.read())

        conn.commit()
        conn.close()
        print(f"Success! Database created at: {DB_PATH}")

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    setup_database()