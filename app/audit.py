from app.database import get_connection


def create_table():
    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        message TEXT,
        intent TEXT,
        confidence REAL,
        agent TEXT
    )
    """)

    conn.commit()
    conn.close()


def log_request(user_id, message, intent, confidence, agent):
    conn = get_connection()

    conn.execute("""
    INSERT INTO audit_log (user_id, message, intent, confidence, agent)
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, message, intent, confidence, agent))

    conn.commit()
    conn.close()


def get_logs():
    conn = get_connection()
    conn.row_factory = lambda cursor, row: {
        "id": row[0],
        "user_id": row[1],
        "message": row[2],
        "intent": row[3],
        "confidence": row[4],
        "agent": row[5],
    }

    rows = conn.execute("SELECT * FROM audit_log").fetchall()
    conn.close()

    return rows