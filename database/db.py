import sqlite3
import os
from datetime import datetime

# Ensure the 'db' directory exists
DB_DIR = 'db'
DB_PATH = os.path.join(DB_DIR, 'bbp_system.db')


def _conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)

    conn = _conn()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT DEFAULT 'user',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    try:
        c.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
    except Exception:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN created_at TEXT DEFAULT CURRENT_TIMESTAMP")
    except Exception:
        pass

    c.execute('''CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        business_name TEXT,
        business_type TEXT DEFAULT '',
        ownership_type TEXT DEFAULT '',
        status TEXT DEFAULT 'Pending',
        risk_level TEXT DEFAULT 'Low',
        submitted_at TEXT DEFAULT CURRENT_TIMESTAMP,
        reviewed_by TEXT DEFAULT '',
        reviewed_at TEXT DEFAULT '',
        notes TEXT DEFAULT '',
        FOREIGN KEY(user_email) REFERENCES users(email)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target TEXT DEFAULT 'admin',
        title TEXT,
        message TEXT,
        is_read INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS permits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        application_id INTEGER,
        user_email TEXT,
        business_name TEXT,
        permit_number TEXT UNIQUE,
        issued_at TEXT DEFAULT CURRENT_TIMESTAMP,
        expires_at TEXT,
        status TEXT DEFAULT 'Active',
        FOREIGN KEY(application_id) REFERENCES applications(id)
    )''')

    # Seed admin
    try:
        c.execute("INSERT OR IGNORE INTO users (email, password, role) VALUES (?, ?, ?)",
                  ("admin@bbp.com", "admin123", "admin"))
        # Ensure existing admin has the admin role
        c.execute("UPDATE users SET role = 'admin' WHERE email = 'admin@bbp.com'")
    except Exception as e:
        print(f"Error seeding database: {e}")

    conn.commit()
    conn.close()


# ── Auth ─────────────────────────────────────────────────
def check_login(email, password):
    conn = _conn()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    result = c.fetchone()
    conn.close()
    return result


def register_user(email, password):
    try:
        conn = _conn()
        c = conn.cursor()
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        conn.close()
        return True, "Account created!"
    except sqlite3.IntegrityError:
        return False, "Email already exists"
    except Exception as e:
        return False, str(e)


# ── Users (admin) ────────────────────────────────────────
def get_all_users():
    conn = _conn()
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT id, email, role, created_at FROM users ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_user(user_id):
    conn = _conn()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()


def update_user_role(user_id, role):
    conn = _conn()
    conn.execute("UPDATE users SET role = ? WHERE id = ?", (role, user_id))
    conn.commit()
    conn.close()


# ── Applications ─────────────────────────────────────────
def get_all_applications():
    conn = _conn()
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM applications ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_user_applications(email):
    conn = _conn()
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM applications WHERE user_email=? ORDER BY id DESC", (email,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_user_permits(email):
    conn = _conn()
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM permits WHERE user_email=? ORDER BY id DESC", (email,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_application_stats():
    conn = _conn()
    c = conn.cursor()
    total = c.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
    pending = c.execute("SELECT COUNT(*) FROM applications WHERE status='Pending'").fetchone()[0]
    approved = c.execute("SELECT COUNT(*) FROM applications WHERE status='Approved'").fetchone()[0]
    rejected = c.execute("SELECT COUNT(*) FROM applications WHERE status='Rejected'").fetchone()[0]
    renewal = c.execute("SELECT COUNT(*) FROM applications WHERE status='Renewal'").fetchone()[0]
    types = c.execute("SELECT COUNT(DISTINCT business_type) FROM applications WHERE business_type != ''").fetchone()[0]
    owners = c.execute("SELECT COUNT(DISTINCT user_email) FROM applications").fetchone()[0]
    high_risk = c.execute("SELECT COUNT(*) FROM applications WHERE risk_level='High'").fetchone()[0]
    rate = round((approved / total * 100), 1) if total > 0 else 0
    conn.close()
    return {
        "total": total, "pending": pending, "approved": approved,
        "rejected": rejected, "renewal": renewal, "types": types,
        "owners": owners, "high_risk": high_risk, "rate": rate,
    }


def update_application_status(app_id, status, reviewer="admin@bbp.com"):
    conn = _conn()
    conn.execute(
        "UPDATE applications SET status=?, reviewed_by=?, reviewed_at=? WHERE id=?",
        (status, reviewer, datetime.now().isoformat(), app_id))
    conn.commit()
    conn.close()


def submit_application(user_email, business_name, business_type="", ownership_type=""):
    conn = _conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO applications (user_email, business_name, business_type, ownership_type) VALUES (?,?,?,?)",
        (user_email, business_name, business_type, ownership_type))
    app_id = c.lastrowid
    # auto-create notification for admin
    c.execute(
        "INSERT INTO notifications (target, title, message) VALUES (?, ?, ?)",
        ("admin", "New Application",
         f"{user_email} submitted a permit application for '{business_name}'."))
    conn.commit()
    conn.close()
    return app_id


# ── Notifications ────────────────────────────────────────
def get_notifications(target="admin"):
    conn = _conn()
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM notifications WHERE target=? ORDER BY id DESC", (target,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mark_all_notifications_read(target="admin"):
    conn = _conn()
    conn.execute("UPDATE notifications SET is_read=1 WHERE target=?", (target,))
    conn.commit()
    conn.close()


def clear_all_notifications(target="admin"):
    conn = _conn()
    conn.execute("DELETE FROM notifications WHERE target=?", (target,))
    conn.commit()
    conn.close()


def add_notification(target, title, message):
    conn = _conn()
    conn.execute(
        "INSERT INTO notifications (target, title, message) VALUES (?,?,?)",
        (target, title, message))
    conn.commit()
    conn.close()


# ── Permits ──────────────────────────────────────────────
def get_all_permits():
    conn = _conn()
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM permits ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def issue_permit(application_id, user_email, business_name):
    import random, string
    pnum = "BP-" + "".join(random.choices(string.digits, k=8))
    exp = datetime(datetime.now().year + 1, 12, 31).isoformat()
    conn = _conn()
    conn.execute(
        "INSERT INTO permits (application_id, user_email, business_name, permit_number, expires_at) VALUES (?,?,?,?,?)",
        (application_id, user_email, business_name, pnum, exp))
    conn.commit()
    conn.close()
    return pnum


# ── Staff / review stats ────────────────────────────────
def get_staff_stats():
    conn = _conn()
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT reviewed_by AS staff,
               SUM(CASE WHEN status='Approved' THEN 1 ELSE 0 END) AS approved,
               SUM(CASE WHEN status='Rejected' THEN 1 ELSE 0 END) AS rejected,
               COUNT(*) AS total
        FROM applications
        WHERE reviewed_by != ''
        GROUP BY reviewed_by
        ORDER BY total DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]
