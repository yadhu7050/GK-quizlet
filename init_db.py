from app import app
from database import db  # Import db from database.py
from models import Users, Categories, Quizzes, Questions, Answers

def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
          # Add initial categories
        category1 = Categories(name="General Knowledge")
        category2 = Categories(name="Science")
        category3 = Categories(name="History")

        db.session.add_all([category1, category2, category3])
        db.session.commit()

        # Add sample quizzes
        quiz1 = Quizzes(title="General Knowledge Quiz", category_id=category1.id)
        quiz2 = Quizzes(title="Science Quiz", category_id=category2.id)

        db.session.add_all([quiz1, quiz2])
        db.session.commit()

        # Add sample questions for the first quiz
        question1 = Questions(quiz_id=quiz1.id, text="What is the capital of France?")
        question2 = Questions(quiz_id=quiz1.id, text="Who wrote 'Hamlet'?")
        question3 = Questions(quiz_id=quiz2.id, text="What is H2O commonly known as?")

        db.session.add_all([question1, question2, question3])
        db.session.commit()

        # Add sample answers
        answer_data = [
            (question1.id, "Berlin", False), (question1.id, "Madrid", False), (question1.id, "Paris", True),
            (question2.id, "Charles Dickens", False), (question2.id, "William Shakespeare", True), (question2.id, "J.K. Rowling", False),
            (question3.id, "Water", True), (question3.id, "Oxygen", False), (question3.id, "Hydrogen", False)
        ]

        answers = [Answers(question_id=qid, text=text, is_correct=correct) for qid, text, correct in answer_data]
        db.session.add_all(answers)
        db.session.commit()

if __name__ == "__main__":
    init_db()
