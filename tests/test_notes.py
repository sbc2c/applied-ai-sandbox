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


def test_new_note_has_starred_false():
    note = notes_service.create_note("Hello", "World")
    assert note["starred"] is False


def test_starred_field_present_in_get_notes():
    notes_service.create_note("A", "B")
    assert "starred" in notes_service.get_notes()[0]


def test_toggle_star_sets_true():
    note = notes_service.create_note("A", "B")
    result = notes_service.toggle_star(note["id"])
    assert result["starred"] is True


def test_toggle_star_toggles_back():
    note = notes_service.create_note("A", "B")
    notes_service.toggle_star(note["id"])
    result = notes_service.toggle_star(note["id"])
    assert result["starred"] is False


def test_toggle_star_unknown_id_returns_none():
    assert notes_service.toggle_star(999) is None


def test_get_notes_filter_starred_returns_only_starred():
    notes_service.create_note("A", "B")
    n2 = notes_service.create_note("C", "D")
    notes_service.toggle_star(n2["id"])
    starred = notes_service.get_notes(filter="starred")
    assert len(starred) == 1
    assert starred[0]["id"] == n2["id"]


def test_get_notes_no_filter_returns_all():
    notes_service.create_note("A", "B")
    notes_service.create_note("C", "D")
    assert len(notes_service.get_notes()) == 2
