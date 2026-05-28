import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import notes_service


def setup_function():
    notes_service.reset()


def test_new_note_has_empty_tags():
    note = notes_service.create_note("Hello", "World")
    assert note["tags"] == []


def test_tags_field_present_in_get_notes():
    notes_service.create_note("A", "B")
    assert "tags" in notes_service.get_notes()[0]


def test_tags_can_be_provided():
    note = notes_service.create_note("A", "B", tags=["work", "urgent"])
    assert note["tags"] == ["work", "urgent"]


def test_existing_notes_not_broken():
    notes_service.create_note("T1", "C1")
    notes_service.create_note("T2", "C2")
    all_notes = notes_service.get_notes()
    assert len(all_notes) == 2
    assert all("tags" in n for n in all_notes)
