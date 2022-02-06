from app import db
from app.models.question import Question
from datetime import datetime 
from flask import Blueprint, request, jsonify, make_response
import os
import requests

questions_bp = Blueprint("questions", __name__, url_prefix=("/questions" ))

@questions_bp.route("", methods=["GET"])
def get_questions():
    if request.method == "GET":
        request_body = request.get_json()
        sort_query = request.args.get("sort")
        # if "unedited_question" not in request_body or request_body["unedited_question"] == "":
        #     return jsonify(details="Invalid request, a question is required."), 400
        # if "topic" not in request_body or request_body["topic"] == "":
        #     return jsonify(details="Invalid request, a question topic is required."), 400

        if sort_query == "desc":
            unedited_question = Question.query.order_by(Question.unedited_question.desc())
        elif sort_query == "asc":
            unedited_question = Question.query.order_by(Question.unedited_question.asc())
        else:
            unedited_question = Question.query.all()

        unedited_question_response = [unedited_question.tojson() for unedited_question in unedited_question]
        return jsonify(unedited_question_response), 200


@questions_bp("", methods=["POST"])
def post_question():
    if request.method == "POST":
        request_body = request.get_json()

        if "unedited_question" not in request_body or "date" not in \
            request_body or "topic" not in request_body:
            return jsonify(details="Invalid data."), 400

        new_question = Question(
            unedited_question=request_body["unedited_question"],
            date=request_body["date"],
            topic=request_body["topic"]
            )

        db.session.add(new_question)
        db.session.commit()

        return {
            "question": {
                "id": new_question.question_id,
                "unedited_question": new_question.unedited_question,
                "edited_question": new_question.edited_question,
                "answer": new_question.answer,
                "date": new_question.date,
                "keywords": new_question.keywords,
                "topic": new_question.topic,
                "research": new_question.research
            }
        }, 201

#     if request.method == "GET":
#         boards = Question.query.all()
#         boards_response = []
#         for board in boards:
#             boards_response.append({
#                 "id" : board.id,
#                 "title" : board.title,
#                 "owner" : board.owner
#             })
#         return jsonify(boards_response), 200


# @questions_bp.route("/<id>", methods=["DELETE"]) 
# def handle_question(id):
#     question = Question.query.get(id)
#     if request.method == "DELETE":
#         db.session.delete(question)
#         db.session.commit()
#         return make_response(f"Board #{id} successfully deleted")


