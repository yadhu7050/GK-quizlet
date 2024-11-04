from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('instance/db.sqlite', timeout=5)
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('start_quiz'))
    return render_template('index.html')

@app.route('/start_quiz')
def start_quiz():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions ORDER BY RANDOM() LIMIT 10')
    questions = cursor.fetchall()

    # Create a list to hold questions with options
    questions_with_options = []

    for question in questions:
        question_dict = dict(question)  # Convert sqlite3.Row to dict
        cursor.execute('SELECT * FROM options WHERE question_id = ? ORDER BY RANDOM() LIMIT 10', (question['id'],))
        options = cursor.fetchall()
        question_dict['options'] = options  # Add options to the question dict
        questions_with_options.append(question_dict)  # Append to the list

    conn.close()
    return render_template('quiz.html', questions=questions_with_options)

@app.route('/submit', methods=['POST'])
def submit():
    conn = get_db_connection()
    cursor = conn.cursor()

    score = 0
    submitted_options = request.form.to_dict(flat=False)

    for question_id, options in submitted_options.items():
        question_id = int(question_id)
        cursor.execute("SELECT id FROM options WHERE question_id = ? AND is_correct = 1", (question_id,))
        correct_option_id = cursor.fetchone()

        if correct_option_id and options:
            if int(options[0]) == correct_option_id[0]:
                score += 1

    cursor.execute("INSERT INTO results (username, score) VALUES (?, ?)",
                   (session['username'], score))
    conn.commit()
    conn.close()

    return redirect(url_for('results'))

@app.route('/results')
def results():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, score FROM results")
    results = cursor.fetchall()
    conn.close()

    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
