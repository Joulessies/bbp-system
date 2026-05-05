import os
import random
from database.db import register_user, submit_application, update_application_status, issue_permit, init_db

print("Initializing database...")
init_db()

print("Seeding Users from bbp_system.sql...")
users = [
    ("juan@example.com", "password123", "Juan", "Dela Cruz"),
    ("mira@example.com", "password123", "Mira", "Applicant"),
    ("mirajulianaa1006@gmail.com", "password123", "Mira Juliana", "Alcantara"),
    ("test_user@example.com", "password123", "Test", "User")
]

for u in users:
    register_user(*u)

print("Seeding Applications from bbp_system.sql...")

def seed_app(user_email, name, btype, address, cap, m_emp, f_emp, fn, ln, contact, gender, status, reviewer):
    app_id = submit_application(
        user_email=user_email, business_name=name, business_type=btype, ownership_type="Single Proprietorship",
        business_address=address, capital_investment=cap, employees_male=m_emp, employees_female=f_emp,
        owner_first_name=fn, owner_last_name=ln, contact_number=contact, email=user_email,
        tin_number="123-456-789", dti_sec_cda_reg_no="DTI-123456", gender=gender
    )
    if status != "Pending":
        update_application_status(app_id, status, reviewer)
    if status in ("Approved", "Ready for Pickup"):
        issue_permit(app_id, user_email, name)
    return app_id

# Juan's Sari-Sari Store
seed_app("juan@example.com", "Juan's Sari-Sari Store", "Retail", "123 Main St, Caloocan", 50000.0, 1, 1, "Juan", "Dela Cruz", "09171234567", "Male", "Returned for Correction", "staff@bbp.com")

# Caloocan Coffee Shop
seed_app("juan@example.com", "Caloocan Coffee Shop", "Food Service", "456 Plaza Ave, Caloocan", 250000.0, 2, 3, "Juan", "Dela Cruz", "09171234567", "Male", "Pending", None)

# Mira's Beauty Parlor
seed_app("mira@example.com", "Mira's Beauty Parlor", "Personal Service", "789 Beauty Way, Caloocan", 120000.0, 0, 3, "Mira", "Applicant", "09189998877", "Female", "Pending", None)

# Quick Fix Electronics
seed_app("mira@example.com", "Quick Fix Electronics", "Automotive", "101 Tech Blvd, Caloocan", 75000.0, 1, 0, "Mira", "Applicant", "09189998877", "Female", "Rejected", "admin@bbp.com")

# Vape Shop
seed_app("mirajulianaa1006@gmail.com", "Vape Shop", "Retail", "Test Address Caloocan", 500000.0, 1, 1, "Mira Juliana", "Alcantara", "09565400304", "Female", "Pending", None)

# Donut
seed_app("mirajulianaa1006@gmail.com", "Donut", "Food Service", "Test Address Caloocan", 10000.0, 0, 1, "Mira Juliana", "Alcantara", "09565400304", "Female", "Pending", None)

# Burger
seed_app("mirajulianaa1006@gmail.com", "Burger", "Food Service", "Test Address Caloocan", 10000.0, 2, 3, "Mira Juliana", "Alcantara", "09565400304", "Female", "Approved", "admin@bbp.com")

# Kapehan Ni Juan
seed_app("mirajulianaa1006@gmail.com", "Kapehan Ni Juan", "Food Service", "Test Address Caloocan", 1000.0, 0, 1, "Juliana", "Alcantara", "09565613", "Female", "Ready for Pickup", "admin@bbp.com")

# Sari Sari
seed_app("mirajulianaa1006@gmail.com", "Sari Sari", "Food Service", "Test Address Caloocan", 10000.0, 0, 0, "Mira", "Alcantara", "09565400304", "Female", "Approved", "admin@bbp.com")

# Python ML Test Gas Station
seed_app("juan@example.com", "Python ML Test Gas Station", "Others", "123 ML Street", 1500000.0, 3, 2, "Juan", "Dela Cruz", "09123456789", "Male", "Rejected", "admin@bbp.com")

# Fixed ML Gas Station
seed_app("test_user@example.com", "Fixed ML Gas Station", "Automotive", "123 Caloocan St, Barangay 183", 2000000.0, 4, 1, "Test", "User", "09123456789", "Male", "Under Review", "staff@bbp.com")

# Food Test
seed_app("mirajulianaa1006@gmail.com", "Food Test", "Food Service", "lot 34, Amparo subd", 500000.0, 0, 0, "Mira", "Alcantara", "09565613", "Female", "Ready for Pickup", "admin@bbp.com")

# SM Fairview
seed_app("mirajulianaa1006@gmail.com", "SM Fairview", "Food Service", "lot 34, Amparo subd", 24324324.0, 6, 6, "Mira", "Alcantara", "09565400304", "Female", "Pending", None)

print("✅ Legacy bbp_system.sql data has been successfully injected into the new SQLite database!")
