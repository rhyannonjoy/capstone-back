from app import db
from flask import current_app

class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unedited_question = db.Column(db.String)
    edited_question = db.Column(db.String)
    answer = db.Column(db.String)
    date = db.Column(db.DateTime, nullable=True)
    keywords = db.Column(db.String)
    topic = db.Column(db.String)
    research = db.Column(db.String)

    def to_json(self):
        return {
                "id": self.question_id,
                "unedited_question" : self.unedited_question,
                "edited_question" : self.edited_question,
                "answer" : self.answer,
                "date" : self.date,
                "keywords" : self.keywords,
                "topic" : self.topic,
                "research" : self.research
        }