# /home/SolutionDevPlug/mysite/app.py
"""
print("🚀 APP LOADED SUCCESSFULLY!")

QuickRideX - Monetized single-file Flask backend (Phase 1 complete)
- Auto DB init, super-admin, wallets, earnings logging
- Dynamic pricing per country, surge multiplier, wallet payouts
- Simulated driver GPS page (client-side movement)
- REST API for users/rides/bookings/earnings
"""

from flask import (
    Flask, render_template, request, redirect, url_for,
    jsonify, send_from_directory, flash, session
)

import smtplib
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

# ---- Email Configuration ----
EMAIL_ADDRESS = "j6o5h0n7p4a6u2l@gmail.com"
EMAIL_PASSWORD = "weznpyyonrgjlobg"
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import sqlite3, os, random, string, math
import geocoder

# Country Auto-Detect (IP)
def detect_user_country():
    try:
        ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        response = requests.get(f"https://ipapi.co/{ip}/json/").json()
        return response.get("country_name")
    except:
        return None

COUNTRY_JSON_PATH = "/home/SolutionDevPlug/mysite/countries.json"

def save_countries_to_json(countries):
    ...

# Optional: IP geolocation (if available)
try:
    import requests
except Exception:
    requests = None

import json
import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, session

COUNTRY_JSON_PATH = "/home/SolutionDevPlug/mysite/countries.json"

# ------- Place this block into app.py (after imports) -------
import os
import re
import sqlite3
import random
import string
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, session, url_for, flash, redirect, render_template, request

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Configuration — adjust if needed
DB_PATH = "/home/SolutionDevPlug/mysite/database.db"
UPLOAD_FOLDER = "/home/SolutionDevPlug/mysite/static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
VERIFICATION_EXPIRY_MINUTES = 60

# ---------- Helpers ----------
def ensure_upload_folder():
    """Ensure uploads folder exists."""
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_code(length=6) -> str:
    return "".join(random.choices(string.digits, k=length))

def send_verification_email(to_email: str, subject: str, body: str):
    """
    Try to call an existing send_email() in your app if present.
    If not found, use a safe fallback (requires SMTP credentials).
    This function intentionally catches exceptions so registration won't crash.
    """

# -------------------------------
# Route: Register
# -------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    import random
    from datetime import datetime, timedelta
    from werkzeug.security import generate_password_hash

    if request.method == "POST":
        # Collect form data
        fullname = request.form.get("fullname", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        country = request.form.get("country", "").strip()
        role = request.form.get("role", "User").strip()
        password = request.form.get("password", "").strip()

        # Extra fields
        gender = request.form.get("gender", "").strip()
        dob = request.form.get("dob", "").strip()
        address = request.form.get("address", "").strip()
        referral = request.form.get("referral", "").strip()
        photo = "default.png"

        # Basic validation
        if not fullname or not email or not phone or not password:
           flash("All required fields must be filled.", "danger")
        return redirect(url_for("register"))

        # Hash password
        hashed_password = generate_password_hash(password)

        # Verification
        verification_code = str(random.randint(100000, 999999))
        code_expiry = (datetime.utcnow() + timedelta(minutes=10)).isoformat()

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Check if email exists
        c.execute("SELECT id FROM users WHERE email = ?", (email,))
        if c.fetchone():
            conn.close()
            flash("Email already registered. Please log in.", "warning")
            return redirect(url_for("login"))

        # Insert user
        c.execute("""
            INSERT INTO users (
                fullname,
                email,
                phone,
                country,
                password,
                role,
                verified,
                verification_code,
                code_expiry,
                gender,
                dob,
                address,
                referral,
                photo,
                wallet_balance,
                rating,
                joined_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            fullname,
            email,
            phone,
            country,
            hashed_password,
            role,
            0,
            verification_code,
            code_expiry,
            gender,
            dob,
            address,
            referral,
            photo,
            0.0,
            0.0,
            datetime.utcnow().isoformat()
        ))

        conn.commit()
        conn.close()

        # Send verification email (safe call)
        try:
            send_verification-email(email,
                 "Verify your account",
                 f"your verification code"
            )
        except exception:
              pass
        flash("Account created! please log in.",
    "success")
        return redirect (ur1_for("login"))

        # Fallback: basic smtplib send (non-blocking, best-effort).
        # NOTE: replace SMTP_* with your SMTP settings if you want fallback to work.
    import smtplib
    from email.message import EmailMessage

    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")  # put in env var
    SMTP_PASS = os.getenv("SMTP_PASS", "")  # put in env var

    if not SMTP_USER or not SMTP_PASS:
            # No SMTP configured — skip sending but return True so registration continues.
            current_app.logger.info("No SMTP credentials configured; skipping fallback email send.")
            return False

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg.set_content(body)

def db_conn():
    """Return sqlite3 connection (use absolute path)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def is_valid_email(email: str) -> bool:
    return bool(re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email))

def normalize_phone(val: str) -> str:
    # naive normalization: remove non-digits. Expect E.164 already or country code will be prepended client-side.
    digits = re.sub(r"\D", "", val or "")
    return digits

# Helper: Auto-detect country from IP
def get_user_country(ip):
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("country_name", "Unknown")
        return "Unknown"
    except Exception:
        return "Unknown"

countries = [
    {"name": "Afghanistan", "code": "AF", "dial": "+93"},
    {"name": "Albania", "code": "AL", "dial": "+355"},
    {"name": "Algeria", "code": "DZ", "dial": "+213"},
    {"name": "Andorra", "code": "AD", "dial": "+376"},
    {"name": "Angola", "code": "AO", "dial": "+244"},
    {"name": "Antigua and Barbuda", "code": "AG", "dial": "+1-268"},
    {"name": "Argentina", "code": "AR", "dial": "+54"},
    {"name": "Armenia", "code": "AM", "dial": "+374"},
    {"name": "Australia", "code": "AU", "dial": "+61"},
    {"name": "Austria", "code": "AT", "dial": "+43"},
    {"name": "Azerbaijan", "code": "AZ", "dial": "+994"},
    {"name": "Bahamas", "code": "BS", "dial": "+1-242"},
    {"name": "Bahrain", "code": "BH", "dial": "+973"},
    {"name": "Bangladesh", "code": "BD", "dial": "+880"},
    {"name": "Barbados", "code": "BB", "dial": "+1246"},
    {"name": "Belarus", "code": "BY", "dial": "+375"},
    {"name": "Belgium", "code": "BE", "dial": "+32"},
    {"name": "Belize", "code": "BZ", "dial": "+501"},
    {"name": "Benin", "code": "BJ", "dial": "+229"},
    {"name": "Bhutan", "code": "BT", "dial": "+975"},
    {"name": "Bolivia", "code": "BO", "dial": "+591"},
    {"name": "Bosnia and Herzegovina", "code": "BA", "dial": "+387"},
    {"name": "Botswana", "code": "BW", "dial": "+267"},
    {"name": "Brazil", "code": "BR", "dial": "+55"},
    {"name": "Brunei", "code": "BN", "dial": "+673"},
    {"name": "Bulgaria", "code": "BG", "dial": "+359"},
    {"name": "Burkina Faso", "code": "BF", "dial": "+226"},
    {"name": "Burundi", "code": "BI", "dial": "+257"},
    {"name": "Cambodia", "code": "KH", "dial": "+855"},
    {"name": "Cameroon", "code": "CM", "dial": "+237"},
    {"name": "Canada", "code": "CA", "dial": "+1"},
    {"name": "Cape Verde", "code": "CV", "dial": "+238"},
    {"name": "Central African Republic", "code": "CF", "dial": "+236"},
    {"name": "Chad", "code": "TD", "dial": "+235"},
    {"name": "Chile", "code": "CL", "dial": "+56"},
    {"name": "China", "code": "CN", "dial": "+86"},
    {"name": "Colombia", "code": "CO", "dial": "+57"},
    {"name": "Comoros", "code": "KM", "dial": "+269"},
    {"name": "Congo (Republic)", "code": "CG", "dial": "+242"},
    {"name": "Congo (DRC)", "code": "CD", "dial": "+243"},
    {"name": "Costa Rica", "code": "CR", "dial": "+506"},
    {"name": "Croatia", "code": "HR", "dial": "+385"},
    {"name": "Cuba", "code": "CU", "dial": "+53"},
    {"name": "Cyprus", "code": "CY", "dial": "+357"},
    {"name": "Czech Republic", "code": "CZ", "dial": "+420"},
    {"name": "Denmark", "code": "DK", "dial": "+45"},
    {"name": "Djibouti", "code": "DJ", "dial": "+253"},
    {"name": "Dominica", "code": "DM", "dial": "+1767"},
    {"name": "Dominican Republic", "code": "DO", "dial": "+1809"},
    {"name": "Ecuador", "code": "EC", "dial": "+593"},
    {"name": "Egypt", "code": "EG", "dial": "+20"},
    {"name": "El Salvador", "code": "SV", "dial": "+503"},
    {"name": "Equatorial Guinea", "code": "GQ", "dial": "+240"},
    {"name": "Eritrea", "code": "ER", "dial": "+291"},
    {"name": "Estonia", "code": "EE", "dial": "+372"},
    {"name": "Eswatini", "code": "SZ", "dial": "+268"},
    {"name": "Ethiopia", "code": "ET", "dial": "+251"},
    {"name": "Fiji", "code": "FJ", "dial": "+679"},
    {"name": "Finland", "code": "FI", "dial": "+358"},
    {"name": "France", "code": "FR", "dial": "+33"},
    {"name": "Gabon", "code": "GA", "dial": "+241"},
    {"name": "Gambia", "code": "GM", "dial": "+220"},
    {"name": "Georgia", "code": "GE", "dial": "+995"},
    {"name": "Germany", "code": "DE", "dial": "+49"},
    {"name": "Ghana", "code": "GH", "dial": "+233"},
    {"name": "Greece", "code": "GR", "dial": "+30"},
    {"name": "Grenada", "code": "GD", "dial": "+1473"},
    {"name": "Guatemala", "code": "GT", "dial": "+502"},
    {"name": "Guinea", "code": "GN", "dial": "+224"},
    {"name": "Guinea-Bissau", "code": "GW", "dial": "+245"},
    {"name": "Guyana", "code": "GY", "dial": "+592"},
    {"name": "Haiti", "code": "HT", "dial": "+509"},
    {"name": "Honduras", "code": "HN", "dial": "+504"},
    {"name": "Hong Kong", "code": "HK", "dial": "+852"},
    {"name": "Hungary", "code": "HU", "dial": "+36"},
    {"name": "Iceland", "code": "IS", "dial": "+354"},
    {"name": "India", "code": "IN", "dial": "+91"},
    {"name": "Indonesia", "code": "ID", "dial": "+62"},
    {"name": "Iran", "code": "IR", "dial": "+98"},
    {"name": "Iraq", "code": "IQ", "dial": "+964"},
    {"name": "Ireland", "code": "IE", "dial": "+353"},
    {"name": "Israel", "code": "IL", "dial": "+972"},
    {"name": "Italy", "code": "IT", "dial": "+39"},
    {"name": "Jamaica", "code": "JM", "dial": "+1876"},
    {"name": "Japan", "code": "JP", "dial": "+81"},
    {"name": "Jordan", "code": "JO", "dial": "+962"},
    {"name": "Kazakhstan", "code": "KZ", "dial": "+7"},
    {"name": "Kenya", "code": "KE", "dial": "+254"},
    {"name": "Kiribati", "code": "KI", "dial": "+686"},
    {"name": "Kuwait", "code": "KW", "dial": "+965"},
    {"name": "Kyrgyzstan", "code": "KG", "dial": "+996"},
    {"name": "Laos", "code": "LA", "dial": "+856"},
    {"name": "Latvia", "code": "LV", "dial": "+371"},
    {"name": "Lebanon", "code": "LB", "dial": "+961"},
    {"name": "Lesotho", "code": "LS", "dial": "+266"},
    {"name": "Liberia", "code": "LR", "dial": "+231"},
    {"name": "Libya", "code": "LY", "dial": "+218"},
    {"name": "Liechtenstein", "code": "LI", "dial": "+423"},
    {"name": "Lithuania", "code": "LT", "dial": "+370"},
    {"name": "Luxembourg", "code": "LU", "dial": "+352"},
    {"name": "Madagascar", "code": "MG", "dial": "+261"},
    {"name": "Malawi", "code": "MW", "dial": "+265"},
    {"name": "Malaysia", "code": "MY", "dial": "+60"},
    {"name": "Maldives", "code": "MV", "dial": "+960"},
    {"name": "Mali", "code": "ML", "dial": "+223"},
    {"name": "Malta", "code": "MT", "dial": "+356"},
    {"name": "Marshall Islands", "code": "MH", "dial": "+692"},
    {"name": "Mauritania", "code": "MR", "dial": "+222"},
    {"name": "Mauritius", "code": "MU", "dial": "+230"},
    {"name": "Mexico", "code": "MX", "dial": "+52"},
    {"name": "Micronesia", "code": "FM", "dial": "+691"},
    {"name": "Moldova", "code": "MD", "dial": "+373"},
    {"name": "Monaco", "code": "MC", "dial": "+377"},
    {"name": "Mongolia", "code": "MN", "dial": "+976"},
    {"name": "Montenegro", "code": "ME", "dial": "+382"},
    {"name": "Morocco", "code": "MA", "dial": "+212"},
    {"name": "Mozambique", "code": "MZ", "dial": "+258"},
    {"name": "Myanmar", "code": "MM", "dial": "+95"},
    {"name": "Namibia", "code": "NA", "dial": "+264"},
    {"name": "Nauru", "code": "NR", "dial": "+674"},
    {"name": "Nepal", "code": "NP", "dial": "+977"},
    {"name": "Netherlands", "code": "NL", "dial": "+31"},
    {"name": "New Zealand", "code": "NZ", "dial": "+64"},
    {"name": "Nicaragua", "code": "NI", "dial": "+505"},
    {"name": "Niger", "code": "NE", "dial": "+227"},
    {"name": "Nigeria", "code": "NG", "dial": "+234"},
    {"name": "North Korea", "code": "KP", "dial": "+850"},
    {"name": "North Macedonia", "code": "MK", "dial": "+389"},
    {"name": "Norway", "code": "NO", "dial": "+47"},
    {"name": "Oman", "code": "OM", "dial": "+968"},
    {"name": "Pakistan", "code": "PK", "dial": "+92"},
    {"name": "Palau", "code": "PW", "dial": "+680"},
    {"name": "Panama", "code": "PA", "dial": "+507"},
    {"name": "Papua New Guinea", "code": "PG", "dial": "+675"},
    {"name": "Paraguay", "code": "PY", "dial": "+595"},
    {"name": "Peru", "code": "PE", "dial": "+51"},
    {"name": "Philippines", "code": "PH", "dial": "+63"},
    {"name": "Poland", "code": "PL", "dial": "+48"},
    {"name": "Portugal", "code": "PT", "dial": "+351"},
    {"name": "Qatar", "code": "QA", "dial": "+974"},
    {"name": "Romania", "code": "RO", "dial": "+40"},
    {"name": "Russia", "code": "RU", "dial": "+7"},
    {"name": "Rwanda", "code": "RW", "dial": "+250"},
    {"name": "Saint Kitts and Nevis", "code": "KN", "dial": "+1869"},
    {"name": "Saint Lucia", "code": "LC", "dial": "+1758"},
    {"name": "Saint Vincent and the Grenadines", "code": "VC", "dial": "+1784"},
    {"name": "Samoa", "code": "WS", "dial": "+685"},
    {"name": "San Marino", "code": "SM", "dial": "+378"},
    {"name": "Sao Tome and Principe", "code": "ST", "dial": "+239"},
    {"name": "Saudi Arabia", "code": "SA", "dial": "+966"},
    {"name": "Senegal", "code": "SN", "dial": "+221"},
    {"name": "Serbia", "code": "RS", "dial": "+381"},
    {"name": "Seychelles", "code": "SC", "dial": "+248"},
    {"name": "Sierra Leone", "code": "SL", "dial": "+232"},
    {"name": "Singapore", "code": "SG", "dial": "+65"},
    {"name": "Slovakia", "code": "SK", "dial": "+421"},
    {"name": "Slovenia", "code": "SI", "dial": "+386"},
    {"name": "Solomon Islands", "code": "SB", "dial": "+677"},
    {"name": "Somalia", "code": "SO", "dial": "+252"},
    {"name": "South Africa", "code": "ZA", "dial": "+27"},
    {"name": "South Korea", "code": "KR", "dial": "+82"},
    {"name": "South Sudan", "code": "SS", "dial": "+211"},
    {"name": "Spain", "code": "ES", "dial": "+34"},
    {"name": "Sri Lanka", "code": "LK", "dial": "+94"},
    {"name": "Sudan", "code": "SD", "dial": "+249"},
    {"name": "Suriname", "code": "SR", "dial": "+597"},
    {"name": "Sweden", "code": "SE", "dial": "+46"},
    {"name": "Switzerland", "code": "CH", "dial": "+41"},
    {"name": "Syria", "code": "SY", "dial": "+963"},
    {"name": "Taiwan", "code": "TW", "dial": "+886"},
    {"name": "Tajikistan", "code": "TJ", "dial": "+992"},
    {"name": "Tanzania", "code": "TZ", "dial": "+255"},
    {"name": "Thailand", "code": "TH", "dial": "+66"},
    {"name": "Togo", "code": "TG", "dial": "+228"},
    {"name": "Tonga", "code": "TO", "dial": "+676"},
    {"name": "Trinidad and Tobago", "code": "TT", "dial": "+1868"},
    {"name": "Tunisia", "code": "TN", "dial": "+216"},
    {"name": "Turkey", "code": "TR", "dial": "+90"},
    {"name": "Turkmenistan", "code": "TM", "dial": "+993"},
    {"name": "Tuvalu", "code": "TV", "dial": "+688"},
    {"name": "Uganda", "code": "UG", "dial": "+256"},
    {"name": "Ukraine", "code": "UA", "dial": "+380"},
    {"name": "United Arab Emirates", "code": "AE", "dial": "+971"},
    {"name": "United Kingdom", "code": "GB", "dial": "+44"},
    {"name": "United States", "code": "US", "dial": "+1"},
    {"name": "Uruguay", "code": "UY", "dial": "+598"},
    {"name": "Uzbekistan", "code": "UZ", "dial": "+998"},
    {"name": "Vatican city", "code": "VA", "dail": "+379"},
]

# ---------- Verify route (code entry) ----------
@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        code = request.form.get("code", "").strip()
        email = session.get("pending_email")
        if not email:
            flash("Session expired. Please register again.", "warning")
            return redirect(url_for("register"))

        try:
            conn = db_conn()
            c = conn.cursor()
            c.execute("SELECT verification_code, code_expiry FROM users WHERE email = ?", (email,))
            row = c.fetchone()
            if not row:
                conn.close()
                flash("User not found.", "danger")
                return redirect(url_for("register"))

            stored_code = row["verification_code"]
            expiry = row["code_expiry"]

            # check expiry
            if expiry:
                try:
                    expiry_dt = datetime.fromisoformat(expiry)
                    if datetime.utcnow() > expiry_dt:
                        conn.close()
                        flash("Verification code expired. Resend a new code.", "warning")
                        return redirect(url_for("verify"))
                except Exception:
                    # ignore parse errors, continue
                    pass

            if code == stored_code:
                c.execute("""
                    UPDATE users SET verified = 1, verification_code = NULL, code_expiry = NULL
                    WHERE email = ?
                """, (email,))
                conn.commit()
                conn.close()
                session.pop("pending_email", None)
                flash("Your account has been verified. You can now log in.", "success")
                return redirect(url_for("login"))
            else:
                conn.close()
                flash("Incorrect verification code. Please try again.", "danger")
                return redirect(url_for("verify"))
        except Exception as e:
            current_app.logger.exception("Verify error")
            flash("Verification failed. Try again later.", "danger")
            return redirect(url_for("verify"))

    # GET -> show verify page
    return render_template("verify.html")

# ---------- Resend verification ----------
@app.route("/resend_verification", methods=["POST"])
def resend_verification():
    email = session.get("pending_email")
    if not email:
        flash("Session expired. Please log in or register again.", "warning")
        return redirect(url_for("login"))

    try:
        new_code = generate_code(6)
        new_expiry = (datetime.utcnow() + timedelta(minutes=VERIFICATION_EXPIRY_MINUTES)).isoformat()

        conn = db_conn()
        c = conn.cursor()
        c.execute("UPDATE users SET verification_code = ?, code_expiry = ? WHERE email = ?", (new_code, new_expiry, email))
        conn.commit()
        conn.close()

        email_subject = "QuickRideX - Your new verification code"
        email_body = f"Your new verification code: {new_code}\nExpires in {VERIFICATION_EXPIRY_MINUTES} minutes."

        send_verification_email(email, email_subject, email_body)
        session["verification_code"] = new_code

        flash("A new verification code has been sent to your email.", "success")
        return render_template("verify.html")
    except Exception as e:
        current_app.logger.exception("Resend verification error")
        flash("Could not resend verification. Try again later.", "danger")
        return redirect(url_for("register"))
# ------- End of block -------

#=============================
# Email verification setup
#=============================
from flask_mail import Mail, Message

def save_countries_to_json(countries):
    try:
        with open(COUNTRY_JSON_PATH, "w") as f:
            json.dump(countries, f, indent=4)
    except Exception as e:
        print("Error saving JSON:", e)

def load_countries_from_json():
    try:
        if os.path.exists(COUNTRY_JSON_PATH):
            with open(COUNTRY_JSON_PATH, "r") as f:
                return json.load(f)
    except Exception as e:
        print("Error loading JSON:", e)
    return None

def load_countries_from_api():
    try:
        url = "https://restcountries.com/v3.1/all"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            cleaned = []
            for c in data:
                name = c.get("name", {}).get("common")
                dial = c.get("idd", {}).get("root")
                suffix = c.get("idd", {}).get("suffixes", [""])
                if name and dial:
                    cleaned.append({
                        "name": name,
                        "dial": dial + suffix[0]
                    })
            cleaned.sort(key=lambda x: x["name"])
            save_countries_to_json(cleaned)
            return cleaned
    except:
        pass
    return None

def get_countries():
    data = load_countries_from_json()
    if data:
        return data

    # fallback to static list
    save_countries_to_json(countries)
    return countries

# --- Initialize Database (Create users table if missing) ---
    import sqlite3
    db_path = "/home/SolutionDevPlug/mysite/database.db"
    with sqlite3.connect(db_path, timeout=10) as conn:
        c = conn.cursor()
        # Create users table if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            fullname TEXT NOT NULL,
            audience TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,

            phone TEXT,
            country TEXT,
            country_code TEXT,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'User',
            wallet_balance REAL DEFAULT 0.0,
            verified INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()
    print("✅ Database initialized successfully.")


# --- Enable Write-Ahead Logging (WAL) Mode ---
def enable_wal_mode():
    import sqlite3
    try:
        with sqlite3.connect("/home/SolutionDevPlug/mysite/database.db", timeout=10) as conn:
            conn.execute("PRAGMA journal_mode=WAL;")
        print("✅ WAL mode enabled for SQLite.")
    except Exception as e:
        print(f"⚠️ Could not enable WAL mode: {e}")


# Call setup on startup
enable_wal_mode()

# Serializer for email verification
serializer = URLSafeTimedSerializer(app.secret_key)

# ---- Email Configuration ----
EMAIL_ADDRESS = "j6o5h0n7p4a6u2l@gmail.com"
EMAIL_PASSWORD = "weznpyyonrgjlobg"

# Flask-Mail configuration
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=EMAIL_ADDRESS,
    MAIL_PASSWORD=EMAIL_PASSWORD,
    MAIL_DEFAULT_SENDER=("QuickRideX", EMAIL_ADDRESS)
)
mail = Mail(app)

# ==================================================
# Email sending helper
# ==================================================
def send_email(to, subject, body):
    """Send an email using Flask-Mail."""
    try:
        msg = Message(subject, recipients=[to], body=body, sender=app.config['MAIL_DEFAULT_SENDER'])
        mail.send(msg)
        print(f"✅ Email sent to {to}")
    except Exception as e:
        print("❌ Email sending failed:", e)

@app.route("/notifications/<audience>")
def get_notifications(audience):
    import sqlite3, json
    conn = sqlite3.connect("/home/SolutionDevPlug/mysite/database.db")
    c = conn.cursor()
    c.execute("SELECT message, created_at FROM notifications WHERE audience = ? ORDER BY id DESC LIMIT 5", (audience,))
    notifications = [{"message": row[0], "time": row[1]} for row in c.fetchall()]
    conn.close()
    return json.dumps(notifications)

# ✅ Make sure this line comes BEFORE app.config settings
app = Flask(__name__)
app.secret_key = "yoursecretkey"
serializer = URLSafeTimedSerializer(app.secret_key)

def get_user_country_and_currency(ip_address):
    """Detect user country and assign correct currency symbol."""
    try:
        g = geocoder.ip(ip_address)
        country = g.country or "Unknown"

        currency_map = {
            "Nigeria": "₦",
            "Ghana": "₵",
            "Kenya": "KSh",
            "United States": "$",
            "United Kingdom": "£",
            "India": "₹",
            "South Africa": "R",
            "Canada": "$",
        }

        symbol = currency_map.get(country, "$")
        return country, symbol
    except Exception as e:
        print(f"Currency detection error: {e}")
        return "Unknown", "$"

# Configure Flask-Mail
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "j6o5h0n7p4a6u2l@gmail.com"  # your Gmail
app.config["MAIL_PASSWORD"] = "ghml kqqa xgpk kwyy"        # your Gmail App Password
app.config["MAIL_DEFAULT_SENDER"] = ("QuickRideX", "j6o5h0n7p4a6u2l@gmail.com")

mail = Mail(app)

def send_verification_email(email):
    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    token = serializer.dumps(email, salt="email-verify")
    verify_link = url_for("verify_email", token=token, _external=True)

    sender_email = EMAIL_ADDRESS
    password = EMAIL_PASSWORD
    receiver_email = email

    subject = "Verify Your QuickRideX Account"

    html_body = """
<html>
  <body style="font-family: Arial; background-color: #f9f9f9; padding: 20px;">
    <h2 style="color:#16a34a;">Welcome to QuickRideX!</h2>
    <p>Hi there,</p>
    <p>Thank you for signing up! Please verify your email below:</p>
    <p style="text-align:center; margin: 30px 0;">
      <a href="{verify_link}" style="background-color:#16a34a; color:white; padding:10px 20px; border-radius:5px; text-decoration:none;">
        Verify My Account
      </a>
    </p>
    <p>If the button doesn't work, copy and paste this link:</p>
    <p style="color:#555;">{verify_link}</p>
    <p>This link expires in 10 minutes.</p>
    <p>© 2025 QuickRideX. All rights reserved.</p>
  </body>
</html>
"""



    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            message_text = message.as_string()
            # Ensure UTF-8 encoding
            message_text = message_text.encode("utf-8", errors="replace").decode("utf-8")
            server.sendmail(sender_email, receiver_email, message_text)
            print(f"✅ Verification email sent to {email}")
    except Exception as e:
        import traceback
        print(f"⚠️ Failed to send verification email: {e}")
        traceback.print_exc()



# -------------------------
# Configurable constants
# -------------------------
APP_NAME = "QuickRideX"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = "/home/SolutionDevPlug/mysite/database.db"
print(f"✅ Using database at: {DB_PATH}")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
ALLOWED_EXT = {"png", "jpg", "jpeg", "pdf"}
MAX_UPLOAD_MB = 6

# Platform commission (adjustable)
PLATFORM_COMMISSION = 0.10   # 10% of fare goes to platform

# Super admin data (initial)
SUPER_ADMIN_EMAIL = "j6o5h0n7p4a6u2l@gmail.com"
SUPER_ADMIN_PASSWORD = "Admin@123"
ADMIN_CREATE_SECRET = "letmein_quickridex"  # change later

# -------------------------
# App and folders
# -------------------------
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))
app.secret_key = os.getenv("FLASK_SECRET", "supersecretkey")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024

# Debug print for logs (safe to remove later)
print("🔎 QuickRideX DB_PATH:", DB_PATH, "exists:", os.path.exists(DB_PATH))

# -------------------------
# DB helpers
# -------------------------
def db_conn():
    # enable row access by index
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = db_conn()
    c = conn.cursor()
    # users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            country TEXT,
            country_code TEXT,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'User',
            verified INTEGER DEFAULT 0,
            verification_code TEXT,
            permission_granted INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # drivers
    c.execute("""
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            license_number TEXT,
            vehicle_type TEXT,
            plate_number TEXT,
            doc_path TEXT,
            verified INTEGER DEFAULT 0,
            submitted_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    # driver locations (for simulation / later real GPS)
    c.execute("""
        CREATE TABLE IF NOT EXISTS driver_locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_id INTEGER,
            lat REAL,
            lng REAL,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(driver_id) REFERENCES drivers(id)
        )
    """)
    # rides
    c.execute("""
        CREATE TABLE IF NOT EXISTS rides (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            driver_id INTEGER,
            origin TEXT,
            destination TEXT,
            ride_type TEXT,
            fare REAL DEFAULT 0,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # wallets
    c.execute("""
        CREATE TABLE IF NOT EXISTS wallets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            balance REAL DEFAULT 0,
            currency TEXT DEFAULT 'GHS',
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    # earnings (platform records each booking)
    c.execute("""
        CREATE TABLE IF NOT EXISTS earnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ride_id INTEGER,
            user_email TEXT,
            driver_email TEXT,
            fare REAL,
            commission REAL,
            driver_earning REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # admin logs
    c.execute("""
        CREATE TABLE IF NOT EXISTS admin_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id INTEGER,
            action TEXT,
            target_name TEXT,
            target_email TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print("✅ DB initialized")

def ensure_super_admin():
    conn = db_conn(); c = conn.cursor()

    # Check if super admin exists
    c.execute("SELECT id FROM users WHERE email=?", (SUPER_ADMIN_EMAIL,))
    row = c.fetchone()

    # If no admin exists, create one
    if not row:
        from werkzeug.security import generate_password_hash
        hashed = generate_password_hash("AdminPass2025")

        c.execute("""
            INSERT INTO users (
                fullname, email, phone, country, country_code,
                password, role, verified, verification_code,
                permission_granted
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "System Administrator",
            SUPER_ADMIN_EMAIL,
            "+233000000000",
            "Ghana",
            "+233",
            hashed,
            "Admin",
            1,
            "",
            1
        ))
        conn.commit()
        print("✔ Super admin created")

        # Create wallet for admin
        c.execute("SELECT id FROM users WHERE email=?", (SUPER_ADMIN_EMAIL,))
        row = c.fetchone()
        admin_id = row[0]

        c.execute("INSERT OR IGNORE INTO wallets (user_id, balance, currency) VALUES (?, ?, ?)",
                  (admin_id, 0, "GHS"))
        conn.commit()

    conn.close()

# -------------------------
# Country + pricing helpers
# -------------------------
def get_countries():
    return [
        ("Ghana", "+233", "GH"),
        ("Nigeria", "+234", "NG"),
        ("Kenya", "+254", "KE"),
        ("South Africa", "+27", "ZA"),
        ("United States", "+1", "US"),
        ("United Kingdom", "+44", "GB"),
        ("India", "+91", "IN"),
    ]

def get_currency_pricing_by_code(code):
    mapping = {
        "NG": {"symbol": "₦", "economy": 500, "comfort": 1000, "luxury": 2000},
        "GH": {"symbol": "₵", "economy": 30, "comfort": 60, "luxury": 120},
        "KE": {"symbol": "KSh", "economy": 150, "comfort": 300, "luxury": 600},
        "ZA": {"symbol": "R", "economy": 40, "comfort": 80, "luxury": 150},
        "US": {"symbol": "$", "economy": 5, "comfort": 10, "luxury": 20},
        "GB": {"symbol": "£", "economy": 4, "comfort": 8, "luxury": 15},
        "IN": {"symbol": "₹", "economy": 100, "comfort": 200, "luxury": 400},
    }
    return mapping.get((code or "").upper(), {"symbol": "GHS", "economy": 30, "comfort": 60, "luxury": 120})

def detect_country_code_from_ip(ip_address):
    try:
        if requests:
            r = requests.get(f"https://ipapi.co/{ip_address}/json/", timeout=2)
            if r.ok:
                return r.json().get("country_code", "GH")
    except Exception:
        pass
    return "GH"

def calculate_fare(ride_type, country_code="GH", distance_km=None):
    pricing = get_currency_pricing_by_code(country_code)
    key = (ride_type or "Economy").lower().capitalize()
    base = pricing.get(key.lower(), None)
    if base is None:
        # fallback
        base = pricing["economy"]
    distance_km = 0 if distance_km is None else float(distance_km)
    fare = base + (distance_km * (base * 0.25))
    hour = datetime.now().hour
    surge = 1.0
    if 7 <= hour <= 9 or 17 <= hour <= 20:
        surge = 1.35
    return round(fare * surge, 2)

# -------------------------
# Wallet & earnings helpers
# -------------------------
def create_wallet_if_missing(user_id, currency="GHS"):
    conn = db_conn(); c = conn.cursor()
    c.execute("SELECT id FROM wallets WHERE user_id=?", (user_id,))
    if not c.fetchone():
        c.execute("INSERT INTO wallets (user_id, balance, currency) VALUES (?, ?, ?)", (user_id, 0.0, currency))
        conn.commit()
    conn.close()

def get_wallet(user_id):
    conn = db_conn(); c = conn.cursor()
    c.execute("SELECT balance, currency FROM wallets WHERE user_id=?", (user_id,))
    r = c.fetchone(); conn.close()
    if r:
        return {"balance": r[0], "currency": r[1]}
    return {"balance": 0.0, "currency": "GHS"}

def change_wallet(user_id, amount):
    conn = db_conn(); c = conn.cursor()
    c.execute("SELECT balance FROM wallets WHERE user_id=?", (user_id,))
    r = c.fetchone()
    if r:
        newbal = r[0] + amount
        c.execute("UPDATE wallets SET balance=?, updated_at=CURRENT_TIMESTAMP WHERE user_id=?", (newbal, user_id))
    else:
        c.execute("INSERT INTO wallets (user_id, balance, currency) VALUES (?, ?, ?)", (user_id, amount, "GHS"))
    conn.commit(); conn.close()

def log_earning(ride_id, user_email, driver_email, fare, commission, driver_earning):
    conn = db_conn(); c = conn.cursor()
    c.execute("""INSERT INTO earnings (ride_id, user_email, driver_email, fare, commission, driver_earning)
                 VALUES (?, ?, ?, ?, ?, ?)""", (ride_id, user_email, driver_email, fare, commission, driver_earning))
    conn.commit(); conn.close()

# ----------------------------------------------
# Helper: Detect user's country and currency
# ----------------------------------------------
import requests

def get_user_country_and_currency(ip_address):
    """Detect user's country and currency using their IP address"""
    try:
        response = requests.get(f"https://ipapi.co/{ip_address}/json/")
        data = response.json()
        country_name = data.get("country_name", "Unknown")
        currency = data.get("currency", "$")
        return country_name, currency
    except Exception as e:
        print("Geo detection error:", e)
        return "Unknown", "$"

# ----------------------------------------------
# Existing code continues below
# ----------------------------------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# -------------------------
# Web routes
# -------------------------
@app.route('/')
def home():
    return render_template('home.html')

# ----------------------------------------------
# ✅ Register Route — Matches your register.html
# ----------------------------------------------
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random, smtplib, ssl, sqlite3, requests

# ---------- Helper: Database ----------
def db_conn():
    return sqlite3.connect("/home/SolutionDevPlug/mysite/database.db")

# ---------- Helper: Detect user's country ----------
def get_user_country_and_currency(ip_address):
    try:
        response = requests.get(f"https://ipapi.co/{ip_address}/json/")
        data = response.json()
        country_name = data.get("country_name", "Unknown")
        currency = data.get("currency", "USD")
        return country_name, currency
    except Exception:
        return "Unknown", "USD"

# -------- Helper: Send Verification Email --------
def send_verification_email(to_email, code):
    smtp_server = "smtp.gmail.com"
    port = 465
    sender_email = EMAIL_ADDRESS
    password = EMAIL_PASSWORD  # Use your Gmail App Password

    subject = "QuickRideX Account Verification"
    message = f"""\
Subject: {subject}

Welcome to QuickRideX!

Your verification code is: {code}

This code will expire in 10 minutes.
If you didn’t sign up, please ignore this email.
"""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, to_email, message)

# --- Login Route (Fixed + Fully Working) ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').strip().lower()
        password = request.form.get('password').strip()

        try:
            conn = sqlite3.connect('/home/SolutionDevPlug/mysite/database.db')
            conn.row_factory = sqlite3.Row   # <-- CRUCIAL FIX
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = c.fetchone()
            conn.close()

            if not user:
                flash("❌ No account found with that email.", "danger")
                return redirect(url_for('login'))

            # Check verification
            if user['verified'] == 0:
                flash("⚠️ Please verify your account before logging in.", "warning")
                return redirect(url_for('verify_code'))

            # Validate password
            if not check_password_hash(user['password'], password):
                flash("❌ Invalid password.", "danger")
                return redirect(url_for('login'))

            # SUCCESS → store session
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            session['user_name'] = user['fullname']
            session['user_role'] = user['role']

            flash(f"👋 Welcome back, {user['fullname']}!", "success")

            # Role-based redirect
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user['role'] == 'driver':
                return redirect(url_for('driver_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))

        except Exception as e:
            import traceback
            traceback.print_exc()
            flash("⚠️ An error occurred during login. Please try again.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/founder_login', methods=['GET', 'POST'])
def founder_login():
    founder_email = "j6o5h0n7p4a6u2l@gmail.com"
    founder_password = "Admin#123"  # ← matches your form exactly

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password') or request.form.get('access_key') or ''

        if not email or not password:
            flash("Please fill in both fields.", "warning")
            return redirect(url_for('founder_login'))

        if email == founder_email and password == founder_password:
            session['email'] = email
            flash("👑 Welcome, founder the Empero!", "success")
            return redirect(url_for('founder_dashboard'))  # ← goes to founder dashboard only
        else:
            flash("❌ Invalid Founder credentials.", "danger")
            return redirect(url_for('founder_login'))

    return render_template('founder_login.html')

# -----------------------------
# Admin Login Route (SuperAdmin)
# -----------------------------
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        login_id = request.form['login_id'].strip().lower()
        password = request.form['password'].strip()

        # 💎 Premium SuperAdmin credentials
        admin_accounts = {
            "superadmin@quickridex.com": "EliteAccess2025",
            "cofounder@quickridex.com": "PrimeAccess2025",
            "support@quickridex.com": "AssistHub2025",
            "j6o5h0n7p4a6u2l@gmail.com": "Admin@123"  # 👑 SuperAdmin
        }

        # Check credentials
        if login_id in admin_accounts and password == admin_accounts[login_id]:
            session['admin_logged_in'] = True
            session['admin_name'] = login_id.split('@')[0]

            if login_id == "j6o5h0n7p4a6u2l@gmail.com":
                session['is_superadmin'] = True
                flash("👑 Welcome SuperAdmin!", "success")
            else:
                session['is_superadmin'] = False
                flash(f'Welcome back, {session["admin_name"]}!', "success")

            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid SuperAdmin credentials. Try again.', 'danger')

    return render_template('admin_login.html')

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_name', None)
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('admin_login'))

@app.route("/logout")
def logout():
    session.clear(); flash("Logged out.", "info"); return redirect(url_for("home"))

@app.route("/user_dashboard")
def user_dashboard():
    if "user_id" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("login"))

    try:
        conn = sqlite3.connect("/home/SolutionDevPlug/mysite/database.db")
        c = conn.cursor()
        c.execute("SELECT fullname, country, currency_symbol FROM users WHERE id = ?", (session["user_id"],))
        user = c.fetchone()
        conn.close()

        if user:
            fullname, country, currency_symbol = user
        else:
            flash("User not found.", "danger")
            return redirect(url_for("logout"))

        return render_template("user_dashboard.html",
                               fullname=fullname,
                               country=country,
                               currency_symbol=currency_symbol)

    except Exception as e:
        print("Dashboard error:", e)
        flash("⚠️ Error loading dashboard.", "danger")
        return redirect(url_for("login"))

# driver dashboard
@app.route("/driver_dashboard")
def driver_dashboard():
    announce_founder_visit("User")  # or "Driver", "Admin", etc.
    # Allow SuperAdmin direct access with Founder Badge
    if session.get("email") == "j6o5h0n7p4a6u2l@gmail.com":
        return render_template(
            "driver_dashboard.html",
            fullname="Founder 👑",
            country="Global",
            balance="Unlimited",
            formatted_balance="∞",
            completed_rides="All",
            pending_rides="All",
            total_earnings="∞",
            verified="Founder Access",
            founder_badge=True
        )

    # Normal driver check
    if "user_id" not in session or session.get("role") != "driver":
        flash("Access denied. Driver login required.", "danger")
        return redirect(url_for("login"))

    fullname, country, currency_symbol, verified = driver

    # ✅ Get driver wallet balance
    c.execute("SELECT balance FROM wallets WHERE user_id = ?", (driver_id,))
    wallet = c.fetchone()
    balance = wallet[0] if wallet else 0.00

    # ✅ Driver stats
    c.execute("SELECT COUNT(*) FROM rides WHERE driver_id = ? AND status = 'completed'", (driver_id,))
    completed_rides = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM rides WHERE driver_id = ? AND status = 'pending'", (driver_id,))
    pending_rides = c.fetchone()[0]

    c.execute("SELECT SUM(fare) FROM rides WHERE driver_id = ? AND status = 'completed'", (driver_id,))
    total_earnings = c.fetchone()[0] or 0.00

    conn.close()

    formatted_balance = f"{currency_symbol}{balance:,.2f}"
    formatted_earnings = f"{currency_symbol}{total_earnings:,.2f}"

    return render_template(
        "driver_dashboard.html",
        fullname=fullname,
        country=country,
        balance=formatted_balance,
        completed_rides=completed_rides,
        pending_rides=pending_rides,
        total_earnings=formatted_earnings,
        verified=verified
    )

# =============================
# ✅ Driver Verification Request System
# =============================
@app.route("/request_verification")
def request_verification():
    if "user_id" not in session or session.get("role") != "driver":
        flash("Login required to request verification.", "danger")
        return redirect(url_for("login"))

    driver_id = session["user_id"]
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Update verification level to pending
    c.execute("UPDATE drivers SET verification_level = 'pending' WHERE id = ?", (driver_id,))
    conn.commit()
    conn.close()

    flash("Verification request sent. Our team will review it shortly.", "info")
    return redirect(url_for("driver_dashboard"))

# driver verify upload
@app.route("/driver/verify", methods=["GET", "POST"])
def driver_verify():
    if "user_id" not in session:
        flash("Please login.", "error"); return redirect(url_for("login"))
    if session.get("role", "").lower() != "driver":
        flash("Access denied.", "error"); return redirect(url_for("login"))
    if request.method == "POST":
        license_number = request.form.get("license_number", "").strip()
        vehicle_type = request.form.get("vehicle_type", "").strip()
        plate_number = request.form.get("plate_number", "").strip()
        file = request.files.get("doc")
        if not license_number or not vehicle_type or not plate_number:
            flash("Please fill all fields.", "error"); return redirect(url_for("driver_verify"))
        doc_path = None
        if file and file.filename:
            if not allowed_file(file.filename):
                flash("Unsupported file type.", "error"); return redirect(url_for("driver_verify"))
            filename = f"{session['user_id']}_drv_{secure_filename(file.filename)}"
            dest = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(dest)
            doc_path = f"static/uploads/{filename}"
        conn = db_conn(); c = conn.cursor()
        c.execute("SELECT id FROM drivers WHERE user_id=?", (session["user_id"],))
        ex = c.fetchone()
        if ex:
            c.execute("""UPDATE drivers SET license_number=?, vehicle_type=?, plate_number=?, doc_path=?, verified=0, submitted_at=CURRENT_TIMESTAMP WHERE user_id=?""",
                      (license_number, vehicle_type, plate_number, doc_path, session["user_id"]))
        else:
            c.execute("""INSERT INTO drivers (user_id, license_number, vehicle_type, plate_number, doc_path, verified) VALUES (?, ?, ?, ?, ?, 0)""",
                      (session["user_id"], license_number, vehicle_type, plate_number, doc_path))
            driver_id = c.lastrowid
            # create initial driver location
            c.execute("INSERT INTO driver_locations (driver_id, lat, lng) VALUES (?, ?, ?)", (driver_id, 5.6037, -0.1870))
        conn.commit(); conn.close()
        flash("Driver verification submitted. Admin will review.", "success")
        return redirect(url_for("driver_dashboard"))
    return render_template("driver_verify.html", current_year=datetime.now().year)

# =========================
# Admin Dashboard (Founder)
# =========================
@app.route("/admin-dashboard")
def admin_dashboard():
    announce_founder_visit("User")  # or "Driver", "Admin", etc.
    try:
        conn = db_conn()
        c = conn.cursor()

        # ========== Get time filter ==========
        now = datetime.now()
        period = request.args.get("period", "today")
        if period == "week":
            start = now - timedelta(days=7)
        elif period == "month":
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        # ========== Total counts ==========
        try:
            c.execute("SELECT COUNT(*) FROM users")
            users_count = c.fetchone()[0]
        except:
            users_count = 0

        try:
            c.execute("SELECT COUNT(*) FROM drivers")
            drivers_count = c.fetchone()[0]
        except:
            drivers_count = 0

        try:
            c.execute("SELECT COUNT(*) FROM rides")
            rides_count = c.fetchone()[0]
        except:
            rides_count = 0

        # ========== Aggregate earnings ==========
        try:
            c.execute("""
                SELECT SUM(commission), SUM(driver_earnings), COUNT(*)
                FROM transactions
                WHERE created_at >= ?
            """, (start.strftime("%Y-%m-%d %H:%M:%S"),))
            row = c.fetchone()
            total_commission = row[0] or 0.0
            total_driver_payouts = row[1] or 0.0
            total_transactions = row[2] or 0
        except Exception as e:
            print("Earnings aggregation error:", e)
            total_commission = 0.0
            total_driver_payouts = 0.0
            total_transactions = 0

        # ========== Recent earnings ==========
        try:
            c.execute("""
                SELECT id, ride_id, user_email, driver_email, commission, driver_earnings, created_at
                FROM transactions
                ORDER BY id DESC
                LIMIT 10
            """)
            recent_earnings = c.fetchall()
        except Exception as e:
            print("Recent earnings error:", e)
            recent_earnings = []

        # ========== Pending drivers ==========
        try:
            c.execute("""
                SELECT id, fullname, email, verification_level, verified
                FROM drivers
                ORDER BY
                    CASE
                        WHEN verification_level = 'pending' THEN 1
                        WHEN verification_level = 'verified' THEN 2
                        WHEN verification_level = 'business' THEN 3
                        ELSE 4
                    END
            """)
            pending_drivers = c.fetchall()
        except Exception as e:
            print("Error fetching drivers:", e)
            pending_drivers = []

        conn.close()

        # ========== Render template ==========
        return render_template(
    "admin_dashboard.html",
    users_count=users_count,
    drivers_count=drivers_count,
    rides_count=rides_count,
    total_commission=total_commission,
    total_driver_payouts=total_driver_payouts,
    total_transactions=total_transactions,
    recent_earnings=recent_earnings,
    is_superadmin=session.get('is_superadmin', False),
    admin_name=session.get('admin_name', 'Admin')
)

    except Exception as e:
        print("Admin dashboard error:", e)
        return "Internal Server Error", 500

# Approve driver
@app.route('/approve_driver/<int:driver_id>', methods=['GET', 'POST'])
def approve_driver(driver_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE drivers SET verified='approved' WHERE id=?", (driver_id,))
    conn.commit()
    conn.close()

    flash('Driver approved successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# Reject driver
@app.route('/reject_driver/<int:driver_id>', methods=['GET', 'POST'])
def reject_driver(driver_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE drivers SET verified='rejected' WHERE id=?", (driver_id,))
    conn.commit()
    conn.close()

    flash('Driver rejected successfully.', 'warning')
    return redirect(url_for('admin_dashboard'))

# ======== SUPERADMIN MANAGEMENT ========

@app.route("/manage_admins")
def manage_admins():
    if not session.get("is_superadmin"):
        flash("Access denied: SuperAdmin privileges required.", "danger")
        return redirect(url_for("overview"))

    conn = db_conn()
    c = conn.cursor()
    c.execute("SELECT id, email, role FROM admins ORDER BY id ASC")
    admins = c.fetchall()
    conn.close()

    return render_template("manage_admins.html", admins=admins, admin_name=session.get("admin_name", "Admin"))

@app.route("/add_admin", methods=["GET", "POST"])
def add_admin():
    announce_founder_visit("User")  # or "Driver", "Admin", etc.
    if not session.get("is_superadmin"):
        flash("Access denied: SuperAdmin privileges required.", "danger")
        return redirect(url_for("overview"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = db_conn()
        c = conn.cursor()
        c.execute("INSERT INTO admins (email, password, role) VALUES (?, ?, ?)", (email, password, "admin"))
        conn.commit()
        conn.close()

        flash("✅ New admin added successfully!", "success")
        return redirect(url_for("manage_admins"))

    return render_template("add_admin.html", admin_name=session.get("admin_name", "Admin"))

@app.route("/delete_admin/<int:admin_id>")
def delete_admin(admin_id):
    if not session.get("is_superadmin"):
        flash("Access denied: SuperAdmin privileges required", "danger")
        return redirect(url_for("overview"))

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM admins WHERE id = ?", (admin_id,))
        conn.commit()
        conn.close()

        flash("🗑️ Admin deleted successfully!", "success")
        return redirect(url_for("manage_admins"))

    except Exception as e:
        print("Delete Admin Error:", e)
        return render_template(
            "error500.html",
            title="Internal Server Error",
            message="Something went wrong while deleting admin.",
            details=str(e)
        ), 500

@app.route('/overview')
def overview():
    announce_founder_visit("User")  # or "Driver", "Admin", etc.
    import sqlite3
    from flask import render_template

    try:
        conn = sqlite3.connect('/home/SolutionDevPlug/mysite/database.db')
        c = conn.cursor()

        # === Total Stats ===
        c.execute("SELECT COUNT(*) FROM users WHERE verified=1")
        active_users = c.fetchone()[0] or 0

        c.execute("SELECT COUNT(*) FROM rides")
        total_rides = c.fetchone()[0] or 0

        c.execute("SELECT IFNULL(SUM(fare), 0) FROM rides")
        total_revenue = c.fetchone()[0] or 0

        # === Recent Rides (10 latest) ===
        c.execute("""
            SELECT
                rides.id,
                u.fullname AS rider_name,
                rides.driver_id,
                rides.origin,
                rides.destination,
                rides.fare,
                rides.status,
                rides.created_at
            FROM rides
            LEFT JOIN users u ON rides.user_id = u.id
            ORDER BY rides.created_at DESC
            LIMIT 10
        """)
        rides = c.fetchall()

        # === Pending Drivers ===
        c.execute("""
            SELECT id, user_id, license_number, vehicle_type, plate_number, verified
            FROM drivers
            WHERE verified=0
        """)
        pending_drivers = c.fetchall()

        conn.close()

        # ✅ Render your real HTML dashboard
        return render_template(
            'overview.html',
            active_users=active_users,
            total_rides=total_rides,
            total_revenue=total_revenue,
            rides=rides,
            pending_drivers=pending_drivers
        )

    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"\n❌ Overview Error: {e}\n{error_trace}")

        # ✅ Premium Error500 page render
        return render_template(
            'error500.html',
            title="Internal Server Error",
            message="Something went wrong while loading the Overview page.",
            details=str(e),
            trace=error_trace
        ), 500

    # Manage driver approvals
@app.route("/manage-driver/<int:driver_id>/<action>")
def manage_driver(driver_id, action):
    if "user_id" not in session or session.get("role") != "admin":
        flash("Access denied.", "danger")
        return redirect(url_for("login"))

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if action == "approve":
        c.execute("UPDATE drivers SET status = 'verified' WHERE id = ?", (driver_id,))
        flash("✅ Driver approved and verified!", "success")
    elif action == "decline":
        c.execute("UPDATE drivers SET status = 'declined' WHERE id = ?", (driver_id,))
        flash("❌ Driver declined.", "danger")
    else:
        flash("Invalid action.", "warning")

    conn.commit()
    conn.close()
    return redirect(url_for("overview"))

@app.route("/create_admin", methods=["GET", "POST"])
def create_admin():
    # ✅ Check if user is logged in and is an admin
    if "user_id" not in session or session.get("role") != "admin":
        flash("🚫 Access denied. Admins only.", "danger")
        return redirect(url_for("login"))

    # ✅ Founder-only access
    founder_email = "j6o5h0n7p4a6u2l@gmail.com"
    if session.get("email") != founder_email:
        flash("🚫 Only the founder can create new admins.", "danger")
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = db_conn()
        c = conn.cursor()
        c.execute(
            "INSERT INTO users (name, email, password, role, verified) VALUES (?, ?, ?, 'admin', 1)",
            (name, email, password)
        )
        conn.commit()
        conn.close()

        flash("✅ New admin account created successfully!", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("create_admin.html")

# Founder Dashboard Route
@app.route("/founder_dashboard")
def founder_dashboard():
    # Only allow the founder to access this page
    founder_email = "jo6sh0n7p4a6ul2l@gmail.com"  # Your founder email

    # Check if user is logged in
    if "email" not in session:
        flash("You must log in first.", "warning")
        return redirect(url_for("login"))

    # Check if user is the founder
    if session["email"] != founder_email:
        flash("Access Denied! Founder privileges only.", "danger")
        return redirect(url_for("overview"))  # or home, or anywhere else you like

    # Database stats
    conn = sqlite3.connect("/home/SolutionDevPlug/mysite/database.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    total_users = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM drivers")
    total_drivers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM rides")
    total_rides = c.fetchone()[0]
    c.execute("SELECT SUM(balance) FROM wallets")
    total_wallets = c.fetchone()[0] or 0
    conn.close()

    founder_name = "System Founder"  # You can dynamically fetch this if needed
    return render_template(
        "founder_dashboard.html",
        founder_name=founder_name,
        total_users=total_users,
        total_drivers=total_drivers,
        total_rides=total_rides,
        total_wallets=total_wallets,
    )

# ---------- Route: Terms ----------
@app.route('/terms')
def terms():
    return render_template('terms.html')

# ---------- Route: Privacy ----------
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

# ---------- Route: Legal ----------
@app.route('/legal')
def legal():
    return render_template('legal.html')

print("Loaded routes:")
print([rule.endpoint for rule in app.url_map.iter_rules()])

@app.route("/validate_email")
def validate_email():
    email = request.args.get("email", "").strip().lower()
    exists = User.query.filter_by(email=email).first() is not None
    return jsonify({"exists": exists})

@app.route("/forgot_password")
def forgot_password():
    return render_template("forgot_password.html")

print("Loaded Routes:", app.url_map)

#------------ CALL INIT_DB LAST ------------
init_db()
# Flask main entry

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082, debug=True)