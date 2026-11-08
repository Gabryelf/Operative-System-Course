"""Отвечает только за подключение к базе данных."""

import pymysql
import pymysql.cursors


class Database:
    def __init__(self, host: str, user: str, password: str, database: str):
        self._config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'cursorclass': pymysql.cursors.DictCursor
        }

    def get_connection(self) -> pymysql.connections.Connection:
        return pymysql.connect(**self._config)
