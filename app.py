from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
from database import db  # Import db from database.py
from models import Users, Categories, Quizzes, Questions, Answers


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'secretkey'
    db.init_app(app)

    with app.app_context():
        from models import Users, Categories, Quizzes, Questions, Answers
        db.create_all()  # Create the database tables

    return app

app = create_app()

@app.route('/')
def home():
    categories = Categories.query.all()
    return render_template('home.html', categories=categories)

@app.route('/category/<int:category_id>')
def category_quizzes(category_id):
    quizzes = Quizzes.query.filter_by(category_id=category_id).all()
    return render_template('category.html', quizzes=quizzes)

@app.route('/quiz/<int:quiz_id>')
def quiz(quiz_id):
    questions = Questions.query.filter_by(quiz_id=quiz_id).all()
    quiz_title = Quizzes.query.get(quiz_id).title
    for question in questions:
        question.options = Answers.query.filter_by(question_id=question.id).all()
    return render_template('quiz.html', questions=questions, quiz_title=quiz_title)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('home'))

@app.route('/submit_quiz/<int:quiz_id>', methods=['POST'])
def submit_quiz(quiz_id):
    if request.method == 'POST':
        total_questions = Questions.query.filter_by(quiz_id=quiz_id).count()
        correct_answers = 0

        for question in Questions.query.filter_by(quiz_id=quiz_id).all():
            user_answer = request.form.get(str(question.id))
            if user_answer and Answers.query.filter_by(id=user_answer, is_correct=True).first():
                correct_answers += 1

        score = (correct_answers / total_questions) * 100
        return render_template('result.html', score=score, total_questions=total_questions)

    return redirect(url_for('home'))  # Redirect if method is not POST

if __name__ == "__main__":
    app.run(debug=True)