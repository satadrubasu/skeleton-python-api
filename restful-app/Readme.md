### Usage Notes 

create_tables.py = initialize aqlite filebased data.db
app.py main flask app file.





## Request Parser 

1. Replacing request.get_json() with parser to pick specific elements from json  
2. Parser is moved to Class level and not Object 

## Setting up sqlite for DB
  1. Enabling the user.py holding User model
  2. Connection and implement methods for db

## Signing Up


## Python import a file logic

Whenever we import a file , all lines execute from that file

 > from user import UserRegister,Register  
  
generally if we dont want to do the runs in the file when getting imported.  
python assigns '__main__' to the __name__ variable when that file is run in python directly  

```
if __name__ == '__main__':
    app.run(port=5000,debug=True)

```

### Flask JWT Configuration - adv 

Change the authentication endpoint (by default, /auth )    
Change the token expiration time (by default, 5 minutes )  
Change the authentication key name (by default, username ).  
Change the authentication response body (by default, only contains access_token ).  