import sqlite3

def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS options (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            option_text TEXT NOT NULL,
            is_correct BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            score INTEGER
        )
    """)

    conn.commit()

def insert_sample_data(conn):
    cursor = conn.cursor()

    # Sample users
    cursor.execute("INSERT INTO users (username) VALUES (?)", ("admin",))
    cursor.execute("INSERT INTO users (username) VALUES (?)", ("user1",))

    # Sample questions and options
    sample_questions = [
        "What is the capital of India?",
        "What is the largest ocean on Earth?",
        "What is the currency of Japan?",
        "What is the powerhouse of the cell?",
        "What is the smallest country in the world?",
        "Which planet is known as the Red Planet?",
        "Who wrote 'Romeo and Juliet'?",
        "What is the hardest natural substance on Earth?"
    ]

    options_data = [
        (1, "New Delhi", True),
        (1, "Mumbai", False),
        (1, "Chennai", False),
        (1, "Kolkata", False),
        (2, "Pacific Ocean", True),
        (2, "Atlantic Ocean", False),
        (2, "Indian Ocean", False),
        (2, "Arctic Ocean", False),
        (3, "Yen", True),
        (3, "Won", False),
        (3, "Dollar", False),
        (3, "Yuan", False),
        (4, "Mitochondria", True),
        (4, "Nucleus", False),
        (4, "Ribosome", False),
        (4, "Golgi apparatus", False),
        (5, "Vatican City", True),
        (5, "Monaco", False),
        (5, "Nauru", False),
        (5, "Malta", False),
        (6, "Mars", True),
        (6, "Venus", False),
        (6, "Earth", False),
        (6, "Jupiter", False),
        (7, "William Shakespeare", True),
        (7, "Charles Dickens", False),
        (7, "Mark Twain", False),
        (7, "J.K. Rowling", False),
        (8, "Diamond", True),
        (8, "Gold", False),
        (8, "Iron", False),
        (8, "Quartz", False),
    ]

    for question_text in sample_questions:
        cursor.execute("INSERT INTO questions (question_text) VALUES (?)", (question_text,))
        question_id = cursor.lastrowid

    for option in options_data:
        cursor.execute("INSERT INTO options (question_id, option_text, is_correct) VALUES (?, ?, ?)", option)

    conn.commit()

if __name__ == "__main__":
    conn = sqlite3.connect('instance/db.sqlite')
    create_tables(conn)
    insert_sample_data(conn)
    conn.close()
