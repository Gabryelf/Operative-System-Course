"""Бизнес-логика. Зависит от интерфейса репозитория (Dependency Inversion)."""

from typing import List
from models import Contact
from repository import IContactRepository


class ContactService:
    def __init__(self, repository: IContactRepository):
        self._repo = repository

    def get_all_contacts(self) -> List[Contact]:
        return self._repo.get_all()

    def add_contact(self, name: str, phone: str) -> None:
        if not name.strip() or not phone.strip():
            raise ValueError("Имя и телефон не могут быть пустыми")
        self._repo.add(Contact(id=None, name=name.strip(), phone=phone.strip()))

    def update_contact(self, contact: Contact) -> None:
        if not contact.name.strip() or not contact.phone.strip():
            raise ValueError("Имя и телефон не могут быть пустыми")
        self._repo.update(contact)

    def delete_contact(self, contact_id: int) -> None:
        self._repo.delete(contact_id)

    def search_contacts(self, query: str) -> List[Contact]:
        if not query.strip():
            return self._repo.get_all()
        return self._repo.search(query.strip())
