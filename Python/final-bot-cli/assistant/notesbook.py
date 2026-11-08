from collections import UserDict
from .note import Note


class NotesBook(UserDict):
    def add_note(self, text, tags=None):
        note = Note(text, tags)
        self.data[text] = note

    def delete_note(self, text):
        if text in self.data:
            del self.data[text]
            return True
        return False

    def edit_note(self, old_text, new_text):
        if old_text in self.data:
            note = self.data.pop(old_text)
            note.edit(new_text)
            self.data[new_text] = note
            return True
        return False

    def find_notes_by_tag(self, tag):
        result = []
        for note in self.data.values():
            if tag.lower() in [t.lower() for t in note.tags]:
                result.append(note)
        return result

    def sort_notes_by_tag(self):
        return sorted(self.data.values(), key=lambda note: ', '.join(note.tags))
