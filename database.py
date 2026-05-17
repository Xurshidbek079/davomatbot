import sqlite3
from contextlib import contextmanager

DB = "attendance.db"

@contextmanager
def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    try:
        yield c
        c.commit()
    finally:
        c.close()

def init_db():
    with conn() as c:
        c.executescript("""
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY,
                telegram_user_id TEXT UNIQUE NOT NULL,
                username TEXT,
                added_by TEXT,
                active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT UNIQUE NOT NULL,
                title TEXT,
                owner_id TEXT,
                active INTEGER DEFAULT 1
            );
            CREATE TABLE IF NOT EXISTS workers (
                id INTEGER PRIMARY KEY,
                telegram_username TEXT NOT NULL,
                telegram_user_id INTEGER,
                full_name TEXT,
                group_chat_id TEXT NOT NULL,
                active INTEGER DEFAULT 1,
                UNIQUE(telegram_username, group_chat_id)
            );
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY,
                worker_username TEXT NOT NULL,
                group_chat_id TEXT NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL,
                raw_response TEXT,
                classified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(worker_username, group_chat_id, date)
            );
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            );
        """)
        c.execute("INSERT OR IGNORE INTO settings VALUES (?,?)",
                  ("daily_message", "Xodimlar, xayrli tong! ✋ Bugun ishda bormi? Iltimos, javob bering."))

# --- Admins ---

def add_admin(user_id, username=None, added_by=None):
    with conn() as c:
        c.execute("INSERT OR REPLACE INTO admins (telegram_user_id,username,added_by,active) VALUES (?,?,?,1)",
                  (str(user_id), username, str(added_by) if added_by else None))

def remove_admin(user_id):
    with conn() as c:
        c.execute("UPDATE admins SET active=0 WHERE telegram_user_id=?", (str(user_id),))

def get_admins():
    with conn() as c:
        return [dict(r) for r in c.execute(
            "SELECT telegram_user_id, username, added_by, created_at FROM admins WHERE active=1").fetchall()]

def is_registered_admin(user_id):
    with conn() as c:
        return c.execute(
            "SELECT 1 FROM admins WHERE telegram_user_id=? AND active=1", (str(user_id),)).fetchone() is not None

# --- Groups ---

def get_group(chat_id):
    with conn() as c:
        row = c.execute("SELECT id, chat_id, title, owner_id, active FROM groups WHERE chat_id=?",
                        (str(chat_id),)).fetchone()
        return dict(row) if row else None

def add_group(chat_id, title=None, owner_id=None):
    with conn() as c:
        if owner_id:
            # Explicit claim: always set the owner
            c.execute("""INSERT INTO groups (chat_id, title, owner_id, active) VALUES (?,?,?,1)
                         ON CONFLICT(chat_id) DO UPDATE SET
                             title=COALESCE(excluded.title, title),
                             owner_id=excluded.owner_id""",
                      (str(chat_id), title, str(owner_id)))
        else:
            # Auto-registration: never overwrite existing owner
            c.execute("""INSERT INTO groups (chat_id, title, active) VALUES (?,?,1)
                         ON CONFLICT(chat_id) DO UPDATE SET title=COALESCE(excluded.title, title)""",
                      (str(chat_id), title))

def remove_group(chat_id):
    with conn() as c:
        c.execute("UPDATE groups SET active=0 WHERE chat_id=?", (str(chat_id),))

def get_active_groups(owner_id=None):
    """Return all active groups. If owner_id given, filter to that owner only."""
    with conn() as c:
        if owner_id:
            return [dict(r) for r in c.execute(
                "SELECT id, chat_id, title, owner_id FROM groups WHERE active=1 AND owner_id=? ORDER BY id",
                (str(owner_id),)).fetchall()]
        return [dict(r) for r in c.execute(
            "SELECT id, chat_id, title, owner_id FROM groups WHERE active=1 ORDER BY id").fetchall()]

def get_group_by_num(num, owner_id=None):
    groups = get_active_groups(owner_id)
    return groups[num - 1] if 1 <= num <= len(groups) else None

# --- Workers ---

def add_worker(username, group_chat_id, full_name=None):
    with conn() as c:
        c.execute("INSERT OR REPLACE INTO workers (telegram_username,group_chat_id,full_name,active) VALUES (?,?,?,1)",
                  (username.lower(), str(group_chat_id), full_name))

def remove_worker(username, group_chat_id):
    with conn() as c:
        c.execute("UPDATE workers SET active=0 WHERE telegram_username=? AND group_chat_id=?",
                  (username.lower(), str(group_chat_id)))

def get_active_workers(group_chat_id):
    with conn() as c:
        return [r[0] for r in c.execute(
            "SELECT telegram_username FROM workers WHERE group_chat_id=? AND active=1",
            (str(group_chat_id),)).fetchall()]

def save_user_id(username, user_id, group_chat_id):
    with conn() as c:
        c.execute("UPDATE workers SET telegram_user_id=? WHERE telegram_username=? AND group_chat_id=?",
                  (user_id, username.lower(), str(group_chat_id)))

# --- Attendance ---

def mark_attendance(username, group_chat_id, date, status, raw_response=None):
    with conn() as c:
        c.execute("INSERT OR REPLACE INTO attendance (worker_username,group_chat_id,date,status,raw_response) VALUES (?,?,?,?,?)",
                  (username.lower(), str(group_chat_id), date, status, raw_response))

def get_today_attendance(group_chat_id, date):
    with conn() as c:
        return {r[0]: r[1] for r in c.execute(
            "SELECT worker_username,status FROM attendance WHERE group_chat_id=? AND date=?",
            (str(group_chat_id), date)).fetchall()}

def get_unresponded(group_chat_id, date):
    return [w for w in get_active_workers(group_chat_id)
            if w not in get_today_attendance(group_chat_id, date)]

def get_attendance_range(group_chat_id, from_date, to_date):
    with conn() as c:
        return {(r[0], r[1]): r[2] for r in c.execute(
            "SELECT worker_username,date,status FROM attendance WHERE group_chat_id=? AND date BETWEEN ? AND ?",
            (str(group_chat_id), from_date, to_date)).fetchall()}

# --- Settings ---

def get_setting(key):
    with conn() as c:
        row = c.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        return row[0] if row else None

def set_setting(key, value):
    with conn() as c:
        c.execute("INSERT OR REPLACE INTO settings VALUES (?,?)", (key, value))


# --- User language preference ---

def get_user_lang(user_id):
    return get_setting(f"lang_{user_id}") or "ru"

def set_user_lang(user_id, lang):
    set_setting(f"lang_{user_id}", lang)
