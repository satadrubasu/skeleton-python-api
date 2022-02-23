from resource.user import UserModel
## In memory table and functions

def authenticate(username,password):
    user = UserModel.find_by_username(username) # if no user found then return None
    if user and user.password == password:
        return user


def identity(payload): ## payload is content of the jwt token
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)