import sqlite3


def main(super_db="/tmp/super_db.sqlite"):
    conn = sqlite3.connect(super_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE supernode (ip INT, port INT)''')
    conn.commit()
    conn.close()

if __name__=="__main__":
    main()
