import sqlite3


DATABASE_NAME = "document_verification.db"


def create_database():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS verification_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            document_id TEXT,
            dob TEXT,
            expiry_date TEXT,
            country TEXT,
            risk_score INTEGER,
            status TEXT,
            problems TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_result(fields, risk_score, status, errors):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    problems = ", ".join(errors)

    cursor.execute("""
        INSERT INTO verification_results
        (name, document_id, dob, expiry_date, country,
         risk_score, status, problems)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        fields["name"],
        fields["document_id"],
        fields["dob"],
        fields["expiry_date"],
        fields["country"],
        risk_score,
        status,
        problems
    ))

    connection.commit()
    connection.close()