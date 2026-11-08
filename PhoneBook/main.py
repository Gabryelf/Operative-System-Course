from database import Database
from repository import MySqlContactRepository
from service import ContactService
from interface import PhoneBookApp


def main():
    db = Database(
        host='localhost',
        user='root',
        password='admin',
        database='PhoneBookDB'
    )
    repository = MySqlContactRepository(db)
    service = ContactService(repository)
    app = PhoneBookApp(service)
    app.mainloop()


if __name__ == '__main__':
    main()
