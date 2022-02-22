from user import User
## In memory table and functions

users = [
    User(1,'aadrit','aadrit')
]

username_mapping = {u.username: u for u in users}

userid_mapping = {u.id: u for u in users}


def authenticate(username,password):
    user = User.find_by_username(username) # if no user found then return None
    if user and user.password == password:
        return user


def identity(payload): ## payload is content of the jwt token
    user_id = payload['identity']
    return User.find_by_id(user_id)