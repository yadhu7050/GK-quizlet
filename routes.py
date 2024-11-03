from flask import render_template, request, redirect, url_for, session, flash
from app import app, db
from models import Users, Categories, Quizzes, Questions, Answers

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
        question.options = Answers.query.filter_by(question_id=question.id).all()  # Fetch answers
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
