import customtkinter as ctk


TERMS_AND_CONDITIONS = """
TERMS AND CONDITIONS OF USE
Barangay 183 Business Permit System
Caloocan City, Philippines
Last Updated: May 2026

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. ACCEPTANCE OF TERMS

By accessing and using the Barangay 183 Business Permit System ("BBP System" or "System"), you acknowledge that you have read, understood, and agree to be bound by these Terms and Conditions. If you do not agree with any part of these terms, you must not use the System.

2. PURPOSE AND SCOPE

The BBP System is an official digital platform developed for Barangay 183, Zone 16, District 1, Caloocan City. It is designed to facilitate the processing, issuance, and management of Barangay Business Clearances in compliance with Republic Act No. 11032 (Ease of Doing Business and Efficient Government Service Delivery Act of 2018).

3. USER REGISTRATION AND ACCOUNTS

3.1. Users must provide accurate, current, and complete information during registration.
3.2. Users are responsible for maintaining the confidentiality of their account credentials.
3.3. Each user may only maintain one (1) active account.
3.4. The Barangay reserves the right to suspend or terminate accounts that violate these terms.
3.5. Users must immediately notify the Barangay of any unauthorized access to their accounts.

4. DATA PRIVACY AND PROTECTION

4.1. The collection, use, and processing of personal data through this System is governed by Republic Act No. 10173 (Data Privacy Act of 2012).
4.2. Personal information collected includes but is not limited to: full name, email address, contact number, business details, and financial information.
4.3. Your data will only be used for the purpose of processing business permit applications and related government services.
4.4. The Barangay shall implement reasonable security measures to protect personal data from unauthorized access, disclosure, or destruction.
4.5. Users have the right to access, correct, and request deletion of their personal information, subject to applicable laws.

5. APPLICATION SUBMISSION

5.1. All information provided in business permit applications must be true, accurate, and complete.
5.2. Submission of fraudulent or misleading information is punishable under applicable Philippine laws.
5.3. The Barangay reserves the right to verify all submitted information and documents.
5.4. Incomplete applications may be returned for correction or rejected.
5.5. Document uploads are limited to image files (PNG, JPG, JPEG, BMP, GIF) with a maximum total size of 500 MB.

6. PROCESSING AND ISSUANCE

6.1. Application processing times may vary depending on the completeness of submissions and current workload.
6.2. The Barangay reserves the right to approve, reject, or request additional information for any application.
6.3. Issuance of a Barangay Business Clearance does not exempt the applicant from securing other permits required by higher government agencies.
6.4. Business clearances are valid until December 31 of the year of issuance and must be renewed annually.

7. FEES AND PAYMENTS

7.1. Applicable fees for Barangay Business Clearances are in accordance with the existing Barangay Revenue Code.
7.2. Official receipts will be issued for all payments made.
7.3. Fees paid are non-refundable unless otherwise provided by law.

8. USER RESPONSIBILITIES

8.1. Users shall comply with all applicable local and national laws and regulations.
8.2. Users shall not attempt to gain unauthorized access to the System or its related systems.
8.3. Users shall not use the System for any unlawful, fraudulent, or malicious purpose.
8.4. Users shall not interfere with or disrupt the System's functionality.

9. INTELLECTUAL PROPERTY

9.1. The BBP System, including its design, features, and content, is the property of Barangay 183, Caloocan City.
9.2. Users may not reproduce, distribute, or create derivative works of the System without prior written consent.

10. LIMITATION OF LIABILITY

10.1. The Barangay shall not be liable for any indirect, incidental, or consequential damages arising from the use of the System.
10.2. The Barangay does not guarantee uninterrupted or error-free operation of the System.
10.3. The System is provided "as is" without warranties of any kind.

11. AMENDMENTS

11.1. The Barangay reserves the right to modify these Terms and Conditions at any time.
11.2. Users will be notified of significant changes through the System's notification feature.
11.3. Continued use of the System after modifications constitutes acceptance of the revised terms.

12. GOVERNING LAW

These Terms and Conditions shall be governed by and construed in accordance with the laws of the Republic of the Philippines. Any disputes arising from these terms shall be resolved through the proper legal channels of Caloocan City.

13. CONTACT INFORMATION

For questions or concerns regarding these Terms and Conditions:

   Barangay 183, Zone 16, District 1
   Caloocan City, Philippines
   Email: barangay183@caloocan.gov.ph
   Office Hours: Monday–Friday, 8:00 AM – 5:00 PM

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

By using the BBP System, you confirm that you have read, understood, and agreed to these Terms and Conditions.
"""


def show_terms_modal(parent):
    """Open a Terms and Conditions modal window."""
    modal = ctk.CTkToplevel(parent)
    modal.title("Terms and Conditions")
    modal.geometry("640x580")
    modal.resizable(False, False)
    modal.grab_set()
    modal.configure(fg_color="#F4F5F7")

    # Header
    hdr = ctk.CTkFrame(modal, fg_color="#E65C00", corner_radius=0, height=55)
    hdr.pack(fill="x")
    hdr.pack_propagate(False)
    ctk.CTkLabel(hdr, text="📜  Terms and Conditions",
                 text_color="white",
                 font=ctk.CTkFont("Segoe UI", 15, "bold")).pack(side="left", padx=20, pady=14)

    # Body
    body = ctk.CTkTextbox(modal, fg_color="white", text_color="#374151",
                          font=ctk.CTkFont("Segoe UI", 10),
                          border_width=1, border_color="#E5E7EB",
                          corner_radius=10, wrap="word")
    body.pack(fill="both", expand=True, padx=16, pady=(12, 0))
    body.insert("1.0", TERMS_AND_CONDITIONS.strip())
    body.configure(state="disabled")

    # Footer
    btn_frame = ctk.CTkFrame(modal, fg_color="#F4F5F7")
    btn_frame.pack(fill="x", padx=16, pady=12)
    ctk.CTkButton(btn_frame, text="I Understand", fg_color="#E65C00", hover_color="#CC5200",
                  text_color="white", font=ctk.CTkFont("Segoe UI", 11, "bold"),
                  height=38, corner_radius=6, command=modal.destroy).pack(side="right")
