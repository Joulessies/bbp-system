import sqlite3
import os
from datetime import datetime

# Ensure the 'db' directory exists
DB_DIR = 'db'
DB_PATH = os.path.join(DB_DIR, 'bbp_system_v2.db')


def _conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)

    conn = _conn()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT DEFAULT '',
        last_name TEXT DEFAULT '',
        email TEXT UNIQUE,
        password TEXT,
        role TEXT DEFAULT 'applicant',
        status TEXT DEFAULT 'Active',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    # Seamlessly migrate older database versions if they are missing newer columns
    for col in [
        "first_name TEXT DEFAULT ''",
        "last_name TEXT DEFAULT ''",
        "role TEXT DEFAULT 'applicant'",
        "status TEXT DEFAULT 'Active'"
    ]:
        try:
            c.execute(f"ALTER TABLE users ADD COLUMN {col}")
        except sqlite3.OperationalError:
            pass

    c.execute('''CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        business_name TEXT NOT NULL,
        business_type TEXT DEFAULT '',
        business_address TEXT DEFAULT '',
        capital_investment REAL DEFAULT 0.0,
        employees_male INTEGER DEFAULT 0,
        employees_female INTEGER DEFAULT 0,
        owner_first_name TEXT DEFAULT '',
        owner_last_name TEXT DEFAULT '',
        contact_number TEXT DEFAULT '',
        email TEXT DEFAULT '',
        tin_number TEXT DEFAULT '',
        dti_sec_cda_reg_no TEXT DEFAULT '',
        ownership_type TEXT DEFAULT '',
        gender TEXT DEFAULT '',
        
        status TEXT DEFAULT 'Pending',
        priority TEXT DEFAULT 'Low',
        completeness_score INTEGER DEFAULT 0,
        risk_level TEXT DEFAULT 'Low',
        remarks TEXT DEFAULT '',
        
        submitted_at TEXT DEFAULT CURRENT_TIMESTAMP,
        reviewed_by TEXT DEFAULT '',
        reviewed_at TEXT DEFAULT '',
        notes TEXT DEFAULT '',
        assigned_to TEXT DEFAULT '',
        FOREIGN KEY(user_email) REFERENCES users(email)
    )''')

    try:
        c.execute("ALTER TABLE applications ADD COLUMN assigned_to TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass

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

    # Seed admin & staff
    try:
        c.execute("INSERT OR IGNORE INTO users (first_name, last_name, email, password, role) VALUES (?, ?, ?, ?, ?)",
                  ("Admin", "System", "admin@bbp.com", "admin123", "admin"))
        c.execute("INSERT OR IGNORE INTO users (first_name, last_name, email, password, role) VALUES (?, ?, ?, ?, ?)",
                  ("Staff", "Member", "staff@bbp.com", "staff123", "staff"))
        
        # Auto-seed mock data if database is empty
        c.execute("SELECT COUNT(*) FROM applications")
        if c.fetchone()[0] == 0:
            print("Auto-seeding mock data from legacy SQL dump...")
            mock_users = [
                ("juan@example.com", "password123", "Juan", "Dela Cruz"),
                ("mira@example.com", "password123", "Mira", "Applicant"),
                ("mirajulianaa1006@gmail.com", "password123", "Mira Juliana", "Alcantara"),
                ("test_user@example.com", "password123", "Test", "User")
            ]
            for u in mock_users:
                c.execute("INSERT OR IGNORE INTO users (email, password, first_name, last_name) VALUES (?, ?, ?, ?)", u)
            
            mock_apps = [
                # email, name, type, address, cap, m_emp, f_emp, fn, ln, contact, gender, status, reviewer
                ("juan@example.com", "Juan's Sari-Sari Store", "Retail", "123 Main St, Caloocan", 50000.0, 1, 1, "Juan", "Dela Cruz", "09171234567", "Male", "Returned for Correction", "staff@bbp.com"),
                ("juan@example.com", "Caloocan Coffee Shop", "Food Service", "456 Plaza Ave, Caloocan", 250000.0, 2, 3, "Juan", "Dela Cruz", "09171234567", "Male", "Pending", None),
                ("mira@example.com", "Mira's Beauty Parlor", "Personal Service", "789 Beauty Way, Caloocan", 120000.0, 0, 3, "Mira", "Applicant", "09189998877", "Female", "Pending", None),
                ("mira@example.com", "Quick Fix Electronics", "Automotive", "101 Tech Blvd, Caloocan", 75000.0, 1, 0, "Mira", "Applicant", "09189998877", "Female", "Rejected", "admin@bbp.com"),
                ("mirajulianaa1006@gmail.com", "Vape Shop", "Retail", "Test Address Caloocan", 500000.0, 1, 1, "Mira Juliana", "Alcantara", "09565400304", "Female", "Pending", None),
                ("mirajulianaa1006@gmail.com", "Donut", "Food Service", "Test Address Caloocan", 10000.0, 0, 1, "Mira Juliana", "Alcantara", "09565400304", "Female", "Pending", None),
                ("mirajulianaa1006@gmail.com", "Burger", "Food Service", "Test Address Caloocan", 10000.0, 2, 3, "Mira Juliana", "Alcantara", "09565400304", "Female", "Approved", "admin@bbp.com"),
                ("mirajulianaa1006@gmail.com", "Kapehan Ni Juan", "Food Service", "Test Address Caloocan", 1000.0, 0, 1, "Juliana", "Alcantara", "09565613", "Female", "Ready for Pickup", "admin@bbp.com"),
                ("mirajulianaa1006@gmail.com", "Sari Sari", "Food Service", "Test Address Caloocan", 10000.0, 0, 0, "Mira", "Alcantara", "09565400304", "Female", "Approved", "admin@bbp.com"),
                ("juan@example.com", "Python ML Test Gas Station", "Others", "123 ML Street", 1500000.0, 3, 2, "Juan", "Dela Cruz", "09123456789", "Male", "Rejected", "admin@bbp.com"),
                ("test_user@example.com", "Fixed ML Gas Station", "Automotive", "123 Caloocan St, Barangay 183", 2000000.0, 4, 1, "Test", "User", "09123456789", "Male", "Under Review", "staff@bbp.com"),
                ("mirajulianaa1006@gmail.com", "Food Test", "Food Service", "lot 34, Amparo subd", 500000.0, 0, 0, "Mira", "Alcantara", "09565613", "Female", "Ready for Pickup", "admin@bbp.com"),
                ("mirajulianaa1006@gmail.com", "SM Fairview", "Food Service", "lot 34, Amparo subd", 24324324.0, 6, 6, "Mira", "Alcantara", "09565400304", "Female", "Pending", None)
            ]
            
            for app in mock_apps:
                c.execute('''INSERT INTO applications (
                    user_email, business_name, business_type, ownership_type, business_address, 
                    capital_investment, employees_male, employees_female, owner_first_name, 
                    owner_last_name, contact_number, email, tin_number, dti_sec_cda_reg_no, gender, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                (app[0], app[1], app[2], "Single Proprietorship", app[3], app[4], app[5], app[6], app[7], app[8], app[9], app[0], "123-456", "DTI-123", app[10], app[11]))
                
                app_id = c.lastrowid
                if app[11] in ("Approved", "Ready for Pickup"):
                    permit_no = f"BBP-2026-{app_id:04d}"
                    c.execute("INSERT OR IGNORE INTO permits (application_id, user_email, business_name, permit_number) VALUES (?, ?, ?, ?)",
                              (app_id, app[0], app[1], permit_no))

    except Exception as e:
        print(f"Error seeding database: {e}")

    # ── Seed permits if table is empty but approved apps exist ──
    try:
        c.execute("SELECT COUNT(*) FROM permits")
        if c.fetchone()[0] == 0:
            c.execute("SELECT id, user_email, business_name FROM applications WHERE status IN ('Approved', 'Ready for Pickup')")
            approved = c.fetchall()
            for app_id, email, bname in approved:
                permit_no = f"BBP-2026-{app_id:04d}"
                exp = datetime(datetime.now().year + 1, 12, 31).isoformat()
                c.execute("INSERT OR IGNORE INTO permits (application_id, user_email, business_name, permit_number, expires_at) VALUES (?,?,?,?,?)",
                          (app_id, email, bname, permit_no, exp))
            if approved:
                print(f"Seeded {len(approved)} permits from approved applications.")
    except Exception as e:
        print(f"Error seeding permits: {e}")

    # ── Seed notifications if table is empty ──
    try:
        c.execute("SELECT COUNT(*) FROM notifications")
        if c.fetchone()[0] == 0:
            notifs = [
                ("admin", "System Initialized", "BBP System has been initialized successfully. Welcome, Administrator!"),
                ("admin", "New Application Received", "Mira Juliana Alcantara submitted a new application for 'Vape Shop'."),
                ("admin", "New Application Received", "Juan Dela Cruz submitted a new application for 'Caloocan Coffee Shop'."),
                ("admin", "Application Approved", "Permit BBP-2026 issued for 'Burger' by Mira Juliana Alcantara."),
                ("admin", "Application Rejected", "Application for 'Quick Fix Electronics' by Mira Applicant was rejected."),
                ("admin", "Staff Activity", "Staff member staff@bbp.com reviewed application #11 (Fixed ML Gas Station)."),
                ("mirajulianaa1006@gmail.com", "Permit Approved", "Your application for 'Burger' has been approved! Permit: BBP-2026-0007"),
                ("mirajulianaa1006@gmail.com", "Application Update", "Your application for 'Kapehan Ni Juan' is ready for pickup."),
                ("juan@example.com", "Application Returned", "Your application for 'Juan's Sari-Sari Store' was returned for correction."),
                ("mira@example.com", "Application Rejected", "Your application for 'Quick Fix Electronics' has been rejected."),
            ]
            for target, title, msg in notifs:
                c.execute("INSERT INTO notifications (target, title, message) VALUES (?,?,?)", (target, title, msg))
            print(f"Seeded {len(notifs)} notifications.")
    except Exception as e:
        print(f"Error seeding notifications: {e}")

    conn.commit()
    conn.close()


# ── Auth ─────────────────────────────────────────────────
def check_login(email, password):
    conn = _conn()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    result = c.fetchone()
    conn.close()
    return dict(result) if result else None


def register_user(email, password, first_name="", last_name=""):
    try:
        conn = _conn()
        c = conn.cursor()
        c.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)", 
                  (first_name, last_name, email, password))
        conn.commit()
        conn.close()
        return True, "Account created!"
    except sqlite3.IntegrityError:
        return False, "Email already exists"
    except Exception as e:
        return False, str(e)


# ── Users (admin) ────────────────────────────────────────
def create_staff_account(email, password, full_name):
    try:
        conn = _conn()
        c = conn.cursor()
        first_name = full_name.split(" ")[0] if " " in full_name else full_name
        last_name = " ".join(full_name.split(" ")[1:]) if " " in full_name else ""
        c.execute("INSERT INTO users (first_name, last_name, email, password, role) VALUES (?, ?, ?, ?, ?)", 
                  (first_name, last_name, email, password, 'staff'))
        conn.commit()
        conn.close()
        return True, "Staff account created successfully!"
    except sqlite3.IntegrityError:
        return False, "Email already exists"
    except Exception as e:
        return False, str(e)

def update_user_status(user_id, status):
    conn = _conn()
    conn.execute("UPDATE users SET status = ? WHERE id = ?", (status, user_id))
    conn.commit()
    conn.close()

def get_all_users():
    conn = _conn()
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT id, first_name, last_name, email, role, status, created_at FROM users ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_user(user_id):
    conn = _conn()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()


def update_user_details(user_id, first_name, last_name, email):
    conn = _conn()
    conn.execute("UPDATE users SET first_name=?, last_name=?, email=? WHERE id=?",
                 (first_name, last_name, email, user_id))
    conn.commit()
    conn.close()


def reset_user_password(user_id, new_password):
    conn = _conn()
    conn.execute("UPDATE users SET password=? WHERE id=?", (new_password, user_id))
    conn.commit()
    conn.close()


def reset_password_by_email(email, new_password):
    conn = _conn()
    conn.row_factory = sqlite3.Row
    user = conn.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()
    if not user:
        conn.close()
        return False, "Email not found in the system."
    conn.execute("UPDATE users SET password=? WHERE email=?", (new_password, email))
    conn.commit()
    conn.close()
    return True, "Password has been reset successfully."


def get_user_activity_log(user_id):
    """Get applications reviewed by or assigned to a user, as an audit trail."""
    conn = _conn()
    conn.row_factory = sqlite3.Row
    user = conn.execute("SELECT email FROM users WHERE id=?", (user_id,)).fetchone()
    if not user:
        conn.close()
        return []
    email = user["email"]
    rows = conn.execute(
        "SELECT id, business_name, status, submitted_at, reviewed_by, reviewed_at, assigned_to "
        "FROM applications WHERE reviewed_by=? OR assigned_to=? ORDER BY submitted_at DESC",
        (email, email)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_avg_processing_days():
    conn = _conn()
    c = conn.cursor()
    c.execute("""SELECT AVG(julianday(reviewed_at) - julianday(submitted_at))
                 FROM applications
                 WHERE reviewed_at != '' AND reviewed_at IS NOT NULL
                 AND submitted_at IS NOT NULL""")
    result = c.fetchone()[0]
    conn.close()
    return round(result, 1) if result else 0


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
    query = """
        SELECT p.*, a.owner_first_name, a.owner_last_name, a.business_address 
        FROM permits p 
        LEFT JOIN applications a ON p.application_id = a.id 
        WHERE p.user_email=? 
        ORDER BY p.id DESC
    """
    rows = conn.execute(query, (email,)).fetchall()
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

def assign_application(app_id, staff_email):
    conn = _conn()
    conn.execute("UPDATE applications SET assigned_to=? WHERE id=?", (staff_email, app_id))
    conn.commit()
    conn.close()


def submit_application(user_email, business_name, business_type="", ownership_type="", 
                       business_address="", capital_investment=0.0, employees_male=0, 
                       employees_female=0, owner_first_name="", owner_last_name="", 
                       contact_number="", email="", tin_number="", dti_sec_cda_reg_no="", gender=""):
    conn = _conn()
    c = conn.cursor()
    
    query = """
        INSERT INTO applications (
            user_email, business_name, business_type, ownership_type,
            business_address, capital_investment, employees_male, employees_female,
            owner_first_name, owner_last_name, contact_number, email, tin_number,
            dti_sec_cda_reg_no, gender
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """
    
    # Calculate a simple Mock ML completeness score based on filled fields
    values = (
        user_email, business_name, business_type, ownership_type,
        business_address, float(capital_investment or 0.0), 
        int(employees_male or 0), int(employees_female or 0),
        owner_first_name, owner_last_name, contact_number, email, 
        tin_number, dti_sec_cda_reg_no, gender
    )
    
    c.execute(query, values)
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

