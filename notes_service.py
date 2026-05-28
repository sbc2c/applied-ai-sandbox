notes = []
_next_id = 1


def create_note(title, content, tags=None):
    global _next_id
    note = {
        "id": _next_id,
        "title": title,
        "content": content,
        "tags": tags if tags is not None else [],
        "starred": False,
    }
    notes.append(note)
    _next_id += 1
    return note


def get_notes(filter=None):
    if filter == "starred":
        return [n for n in notes if n["starred"]]
    return notes


def toggle_star(note_id):
    for note in notes:
        if note["id"] == note_id:
            note["starred"] = not note["starred"]
            return note
    return None


def reset():
    global notes, _next_id
    notes = []
    _next_id = 1
