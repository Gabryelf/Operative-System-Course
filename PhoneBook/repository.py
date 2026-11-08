"""Интерфейс репозитория. Сервис зависит от него, а не от MySQL напрямую."""

from abc import ABC, abstractmethod
from typing import List
from models import Contact
from database import Database


class IContactRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[Contact]:
        ...

    @abstractmethod
    def add(self, contact: Contact) -> None:
        ...

    @abstractmethod
    def update(self, contact: Contact) -> None:
        ...

    @abstractmethod
    def delete(self, contact_id: int) -> None:
        ...

    @abstractmethod
    def search(self, query: str) -> List[Contact]:
        ...


"""Реализация репозитория для MySQL."""


class MySqlContactRepository(IContactRepository):
    def __init__(self, db: Database):
        self._db = db

    def get_all(self) -> List[Contact]:
        with self._db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, phone FROM contacts ORDER BY id")
                rows = cur.fetchall()
                return [Contact(id=r['id'], name=r['name'], phone=r['phone']) for r in rows]

    def add(self, contact: Contact) -> None:
        with self._db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                    (contact.name, contact.phone)
                )
            conn.commit()

    def update(self, contact: Contact) -> None:
        with self._db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE contacts SET name = %s, phone = %s WHERE id = %s",
                    (contact.name, contact.phone, contact.id)
                )
            conn.commit()

    def delete(self, contact_id: int) -> None:
        with self._db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
            conn.commit()

    def search(self, query: str) -> List[Contact]:
        with self._db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, name, phone FROM contacts WHERE name LIKE %s OR phone LIKE %s ORDER BY id",
                    (f'%{query}%', f'%{query}%')
                )
                rows = cur.fetchall()
                return [Contact(id=r['id'], name=r['name'], phone=r['phone']) for r in rows]