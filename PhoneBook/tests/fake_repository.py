"""Репозиторий-заглушка для тестов. Не требует MySQL."""

from repository import IContactRepository
from models import Contact
from typing import List


class FakeContactRepository(IContactRepository):
    def __init__(self):
        self._contacts = []
        self._next_id = 1

    def get_all(self) -> List[Contact]:
        return self._contacts.copy()

    def add(self, contact: Contact) -> None:
        contact.id = self._next_id
        self._next_id += 1
        self._contacts.append(contact)

    def update(self, contact: Contact) -> None:
        for i, c in enumerate(self._contacts):
            if c.id == contact.id:
                self._contacts[i] = contact
                return
        raise ValueError("Контакт не найден")

    def delete(self, contact_id: int) -> None:
        self._contacts = [c for c in self._contacts if c.id != contact_id]

    def search(self, query: str) -> List[Contact]:
        q = query.lower()
        return [c for c in self._contacts if q in c.name.lower() or q in c.phone]
