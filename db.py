from tinydb import TinyDB, Query
from tinydb.table import Document


class UserDB:
    def __init__(self, file_name: str) -> None:
        self.db = TinyDB(file_name, indent=4)
        self.users = self.db.table('users')
        self.cart = self.db.table('cart')

    def is_user(self, chat_id: str) -> bool:
        return self.users.contains(doc_id=chat_id)

    def add_user(self, chat_id: str, first_name: str, last_name: str, username: str) -> int:
        if self.is_user(chat_id):
            return False

        user = Document(
            value={
                'first_name': first_name,
                'last_name': last_name,
                'username': username
            },
            doc_id=chat_id
        )
        return self.users.insert(user)

    def add_currency(self, chat_id, currency):
        fields = {'currency': currency}
        self.users.update(fields=fields, doc_ids=[chat_id])