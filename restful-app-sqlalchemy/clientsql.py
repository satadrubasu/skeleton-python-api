import sqlite3

insertcount = 1
def createSchemas():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    # MUST BE INTEGER
    # This is the only place where int vs INTEGER matters—in auto-incrementing columns
    create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
    cursor.execute(create_table)

    create_table = "CREATE TABLE IF NOT EXISTS items (name text PRIMARY KEY, price real)"
    cursor.execute(create_table)

    connection.commit()
    connection.close()

#####
def insert_mock_data():
    global insertcount
    connection = sqlite3.connect('data.db')
    user1 = (insertcount,f'user-{insertcount}','pass')
    insertcount+=1
    user2 = (insertcount, f'user-{insertcount}', 'pass')
    insertcount += 1
    users = [user1,user2]
    cursor = connection.cursor()
    insert_query = "INSERT INTO users VALUES (?,?,?)"
    cursor.executemany(insert_query,users)
    connection.commit()
    connection.close()

def select_cmd():
    print("----SELECT------")
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    query = "SELECT * FROM users"
    rows = cursor.execute(query)
    for row in rows:
        print(f'Record : {row}')
    connection.commit()
    connection.close()

def delete_all():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    query = "Delete FROM users"
    cursor.execute()
    connection.commit()
    connection.close()

if __name__ == '__main__':
    print("Utility Methods to setup local db and operations")

    msg = " \n\n ========  Press numbered options: \n \
  1. Create tables  | 2. Delete all rows |  3. Insert 2 rows  | 4. Show all records \n --[Option]--> "

    x = 0
    while x < 6:
        x = int(input(msg))

        if x == 1:
            print(f"-- Creating tables in data.db--")
            createSchemas()
        elif x == 2:
            print(f"-- Deleting all rows ")
            delete_all()
        elif x == 3:
            print(f"")
            insert_mock_data()
        elif x == 4:
            print(f"---- Showing Records ----")
            select_cmd()
        else:
            print("-- Invalid option - Exitt ----")
            exit()