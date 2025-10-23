import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'projects.db')


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the projects table if it doesn't exist."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            imagefile TEXT NOT NULL
        )
    ''')
    conn.commit()
    # Seed with example rows if empty
    cur.execute('SELECT COUNT(*) as cnt FROM projects')
    row = cur.fetchone()
    if row and row['cnt'] == 0:
        cur.execute('INSERT INTO projects (title, description, imagefile) VALUES (?,?,?)',
                    ('Business Presentations Final Capstone',
                     'Created a Pitch and Slide Deck for a fictional product launch, incorporating market research and competitive analysis.',
                     'BusPres.png'))
        cur.execute('INSERT INTO projects (title, description, imagefile) VALUES (?,?,?)',
                    ('Marketing Research Team Presentation',
                     'Developed a comprehensive marketing research presentation, utilizing data visualization techniques to convey insights on consumer behavior and market trends.',
                     'MarketRes.png'))
        conn.commit()
    conn.close()


def get_projects():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, title, description, imagefile FROM projects ORDER BY id DESC')
    rows = cur.fetchall()
    conn.close()
    # convert sqlite Row objects to dicts for Jinja
    return [dict(r) for r in rows]


def add_project(title, description, imagefile):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO projects (title, description, imagefile) VALUES (?,?,?)',
                (title, description, imagefile))
    conn.commit()
    conn.close()


# ensure DB exists when module is imported
init_db()
