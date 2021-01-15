import sqlite3
BUILD_PATH = "./database/setup/build.sql"
conn = sqlite3.connect("database/database.db")
c = conn.cursor()
def runscript(path):
    with open(path, "r") as script:
        c.executescript(script.read())
        conn.commit()
        conn.close()

runscript(BUILD_PATH)