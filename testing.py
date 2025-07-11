
from admin.model import UserUpdate
from user.model import User, UserCreate

user_data = UserUpdate(username="mani", password="hi")
user_dump = user_data.model_dump(exclude_unset=True)
print(user_dump)

user = User(username="mani", password_hash=b'hash', is_admin=True)
user.sqlmodel_update(user_dump, update={
    "password_hash": "hash2"
})
print(user)

