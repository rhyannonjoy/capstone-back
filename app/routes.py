from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.question import Question


questions_bp = Blueprint("questions", __name__, url_prefix="/questions")


@questions_bp.route("", methods=["GET", "POST"])
def handle_questions():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or  request_body["title"] == "":
            return jsonify(details="Invalid request, a title is required."), 400
        if "owner" not in request_body or request_body["owner"] == "":
            return jsonify(details="Invalid request, an owner is required."), 400

        new_board = Question(title=request_body["title"], owner=request_body["owner"])



        db.session.add(new_board)
        db.session.commit()

        return jsonify({"board":{"board_id": new_board.id, "owner": new_board.owner, "title": new_board.title}}), 201

    if request.method == "GET":
        boards = Question.query.all()
        boards_response = []
        for board in boards:
            boards_response.append({
                "id" : board.id,
                "title" : board.title,
                "owner" : board.owner
            })
        return jsonify(boards_response), 200


@questions_bp.route("/<id>", methods=["DELETE"]) 
def handle_question(id):
    question = Question.query.get(id)
    if request.method == "DELETE":
        db.session.delete(question)
        db.session.commit()
        return make_response(f"Board #{id} successfully deleted")


