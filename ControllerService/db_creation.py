import sqlite3

TIMER_FILEPATH = 'timers.db'

def sqlite3_create_db():
    conn = sqlite3.connect(TIMER_FILEPATH)
    c = conn.cursor()

    c.execute('''CREATE TABLE devices
                 (alias TEXT NOT NULL PRIMARY KEY, uuid TEXT NOT NULL, is_online INTEGER)''')
    c.execute('''CREATE TABLE timers
                 (tid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, alias TEXT NOT NULL, time TEXT NOT NULL, date TEXT, status TEXT NOT NULL, comment TEXT, deletable INTEGER)''')

    c.execute("INSERT INTO devices VALUES ('7E', '192.168.8.103', 1)")
    c.execute("INSERT INTO devices VALUES ('CA', '192.168.8.104', 1)")
    c.execute("INSERT INTO devices VALUES ('DF', '192.168.8.101', 1)")
    c.execute("INSERT INTO devices VALUES ('BE', '192.168.8.106', 1)")
    c.execute("INSERT INTO devices VALUES ('F6', '192.168.8.106', 1)")
    #c.execute("INSERT INTO devices VALUES ('', 'AGENT007', 1)")
    #c.execute("INSERT INTO devices VALUES ('JB', 'AGENT007', 1)")
    #c.execute("INSERT INTO timers (alias,time,date,status) VALUES ('JB', '00:00', '', 'ON')")

    conn.commit()

    conn.close()

sqlite3_create_db()
