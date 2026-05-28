notes = []
_next_id = 1


def create_note(title, content, tags=None):
    global _next_id
    note = {
        "id": _next_id,
        "title": title,
        "content": content,
        "tags": tags if tags is not None else [],
    }
    notes.append(note)
    _next_id += 1
    return note


def get_notes():
    return notes


def reset():
    global notes, _next_id
    notes = []
    _next_id = 1
