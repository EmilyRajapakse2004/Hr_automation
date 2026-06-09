import sqlite3

DB_NAME = "hr_system.db"


def get_connection():
    return sqlite3.connect(DB_NAME)