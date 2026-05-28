from flask import Flask, jsonify, request
import notes_service

app = Flask(__name__)


@app.get("/notes")
def list_notes():
    filter_param = request.args.get("filter")
    return jsonify(notes_service.get_notes(filter=filter_param))


@app.post("/notes")
def create_note():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    content = data.get("content")
    if not title or not content:
        return jsonify({"error": "title and content required"}), 400
    note = notes_service.create_note(title, content, tags=data.get("tags"))
    return jsonify(note), 201


@app.patch("/notes/<int:note_id>/star")
def star_note(note_id):
    note = notes_service.toggle_star(note_id)
    if note is None:
        return jsonify({"error": "Note not found"}), 404
    return jsonify(note)


if __name__ == "__main__":
    app.run(debug=True)
