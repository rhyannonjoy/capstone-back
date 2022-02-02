from app import db

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unchecked_question = db.Column(db.String)
    checked_question = db.Column(db.String)
    answer = db.Column(db.String)
    #date = db.Column(#need to get a date in here)
    keywords = db.Column(db.String)
    topic = db.Column(db.String)
    research = db.Column(db.String)