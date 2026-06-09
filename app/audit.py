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

    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM audit_log").fetchall()

    conn.close()

    return [
        {
            "id": r[0],
            "user_id": r[1],
            "message": r[2],
            "intent": r[3],
            "confidence": r[4],
            "agent": r[5],
        }
        for r in rows
    ]