"""Модель контакта. Отвечает только за хранение данных."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Contact:
    id: Optional[int]
    name: str
    phone: str
