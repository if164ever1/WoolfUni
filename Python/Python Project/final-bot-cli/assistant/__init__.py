# assistant/__init__.py

from .record import Record
from .address_book import AddressBook
from .notesbook import NotesBook
from .note import Note
from .serialization import save_data, load_data, save_notes, load_notes
from .fields import Name, Phone, Birthday, Field