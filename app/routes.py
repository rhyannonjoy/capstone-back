from app import db
from app.models.question import Question
from flask import Blueprint, request, jsonify, make_response


questions_bp = Blueprint("questions", __name__, url_prefix="/questions")


@questions_bp.route("", methods=["GET"])
def get_questions():
    if request.method == "GET":
        sort_query = request.args.get("sort")

        if sort_query == "desc":
            unedited_question = Question.query.order_by(Question.unedited_question.desc())
        elif sort_query == "asc":
            unedited_question = Question.query.order_by(Question.unedited_question.asc())
        else:
            unedited_question = Question.query.all()

        unedited_question_response = [unedited_question.to_json() for unedited_question in unedited_question]
        return jsonify(unedited_question_response), 200


@questions_bp.route("", methods=["POST"])
def post_question():
    if request.method == "POST":
        request_body = request.get_json()

        if "unedited_question" not in request_body or request_body["unedited_question"] == "":
            return jsonify(details="Invalid request, a question is required."), 400
        if "date" not in request_body or request_body["date"] == "":
            return jsonify(details="Invalid request, a question date is required."), 400
        if "topic" not in request_body or request_body["topic"] == "":
            return jsonify(details="Invalid request, a question topic is required."), 400

        new_question = Question(
            unedited_question=request_body["unedited_question"],
            edited_question=request_body["edited_question"],
            answer=request_body["answer"],
            date=request_body["date"],
            keywords=request_body["keywords"],
            topic=request_body["topic"],
            research=request_body["research"]
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


@questions_bp.route("/<question_id>", methods=["GET", "PUT", "DELETE"])
def handle_question_id(question_id):
    question = Question.query.get(question_id)
    if question == None:
        return (""), 404

    if request.method == "GET":
        return {
            "question": {
                "id": question.question_id,
                "unedited_question": question.unedited_question,
                "edited_question": question.edited_question,
                "answer": question.answer,
                "date": question.date,
                "keywords": question.keywords,
                "topic": question.topic,
                "research": question.research
            }}, 200

    if request.method == "PUT":
        form_data = request.get_json()

        question.unedited_question=form_data["unedited_question"],
        question.edited_question=form_data["edited_question"],
        question.answer=form_data["answer"],
        question.date=form_data["date"],
        question.keywords=form_data["keywords"],
        question.topic=form_data["topic"],
        question.research=form_data["research"]
        db.session.commit()

        return {
            "question": {
                "id": question.question_id,
                "unedited_question": question.unedited_question,
                "edited_question": question.edited_question,
                "answer": question.answer,
                "date": question.date,
                "keywords": question.keywords,
                "topic": question.topic,
                "research": question.research
            }}, 200

    elif request.method == "DELETE":
        db.session.delete(question)
        db.session.commit()

        return jsonify({
            "details": f'Question {question.question_id} "{question.topic}" successfully deleted.'
            }), 200