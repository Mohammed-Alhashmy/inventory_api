import sqlite3

def build_database():

    connect = sqlite3.connect('inventory.db')

    with open('schema.sql', 'r') as file :
        shema_script = file.read()


    cr = connect.cursor()
    cr.executescript(shema_script)

    connect.commit()
    connect.close()

    print("Database built successfully!")

if __name__ == "__main__":
    build_database()