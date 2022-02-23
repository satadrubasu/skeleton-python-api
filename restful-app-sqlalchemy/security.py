from resources.user import UserModel
## In memory table and functions

users = [
    UserModel(1,'aadrit','aadrit')
]

username_mapping = {u.username: u for u in users}

userid_mapping = {u.id: u for u in users}


def authenticate(username,password):
    user = UserModel.find_by_username(username) # if no user found then return None
    if user and user.password == password:
        return user


def identity(payload): ## payload is content of the jwt token
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)