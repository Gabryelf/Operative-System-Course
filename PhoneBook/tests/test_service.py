"""Фикстура: создаёт сервис с чистым фейковым репозиторием перед каждым тестом."""

import pytest
from service import ContactService
from .fake_repository import FakeContactRepository


@pytest.fixture
def service():
    repo = FakeContactRepository()
    return ContactService(repo)


# --- Тесты добавления ---

def test_add_contact_success(service):
    service.add_contact("Иван", "+79991234567")
    contacts = service.get_all_contacts()
    assert len(contacts) == 1
    assert contacts[0].name == "Иван"
    assert contacts[0].phone == "+79991234567"
    assert contacts[0].id == 1


def test_add_contact_strips_whitespace(service):
    service.add_contact("  Анна  ", "  123  ")
    contacts = service.get_all_contacts()
    assert contacts[0].name == "Анна"
    assert contacts[0].phone == "123"


def test_add_contact_empty_name_raises_error(service):
    with pytest.raises(ValueError, match="Имя и телефон не могут быть пустыми"):
        service.add_contact("", "123")


def test_add_contact_empty_phone_raises_error(service):
    with pytest.raises(ValueError, match="Имя и телефон не могут быть пустыми"):
        service.add_contact("Иван", "   ")


# --- Тесты поиска ---

def test_search_finds_by_name(service):
    service.add_contact("Иван Петров", "111")
    service.add_contact("Анна Смирнова", "222")
    results = service.search_contacts("Иван")
    assert len(results) == 1
    assert results[0].name == "Иван Петров"


def test_search_finds_by_phone(service):
    service.add_contact("Иван", "+79990001122")
    results = service.search_contacts("999")
    assert len(results) == 1


def test_search_empty_query_returns_all(service):
    service.add_contact("Иван", "111")
    service.add_contact("Анна", "222")
    results = service.search_contacts("   ")
    assert len(results) == 2


# --- Тесты обновления ---

def test_update_contact_success(service):
    service.add_contact("Иван", "111")
    contact = service.get_all_contacts()[0]
    contact.name = "Иван Новый"
    contact.phone = "999"
    service.update_contact(contact)
    updated = service.get_all_contacts()[0]
    assert updated.name == "Иван Новый"
    assert updated.phone == "999"


def test_update_contact_empty_name_raises_error(service):
    service.add_contact("Иван", "111")
    contact = service.get_all_contacts()[0]
    contact.name = ""
    with pytest.raises(ValueError, match="Имя и телефон не могут быть пустыми"):
        service.update_contact(contact)


# --- Тесты удаления ---

def test_delete_contact_success(service):
    service.add_contact("Иван", "111")
    contact_id = service.get_all_contacts()[0].id
    service.delete_contact(contact_id)
    assert len(service.get_all_contacts()) == 0