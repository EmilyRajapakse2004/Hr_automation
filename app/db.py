import sqlite3

conn = sqlite3.connect("../hr_system.db")
cursor = conn.cursor()

rows = cursor.execute("SELECT * FROM audit_log").fetchall()

for row in rows:
    print(row)

conn.close()