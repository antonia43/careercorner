import streamlit as st
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
import re
import os
from dotenv import load_dotenv
from pathlib import Path
import tempfile
from utils.database import init_database

load_dotenv()

DB_PATH = Path(tempfile.gettempdir()) / "career_corner.db"

def init_db():
    return init_database()

def get_user_by_username(conn, username):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username.lower(), username.lower()))
    row = cur.fetchone()
    if row:
        return {
            "id": row[0], "username": row[1], "display_name": row[2],
            "email": row[3], "password_hash": row[4], "remember_token": row[5]
        }
    return None

def create_user(conn, username, display_name, email, password):
    try:
        pw_hash = generate_password_hash(password)
        now_utc = datetime.now(timezone.utc).isoformat()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, display_name, email, password_hash, created_at) VALUES (?, ?, ?, ?, ?)",
            (username.lower(), display_name, email.lower(), pw_hash, now_utc)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login_ui(conn=None):
    if conn is None:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    
    st.subheader("Login")
    username = st.text_input("Username/Email", key="login_username").strip().lower()
    password = st.text_input("Password", type="password", key="login_password")
    remember = st.checkbox("Remember me")

    if st.button("Login"):
        user = get_user_by_username(conn, username)
        if user and check_password_hash(user["password_hash"], password):
            st.session_state.logged_in = True
            st.session_state.username = user["email"]  # For Langfuse
            st.session_state.user_display_name = user["display_name"]
            st.session_state.user = user
            st.success(f"Welcome back, {user['display_name']}!")
            st.rerun()
        else:
            st.error("Invalid username or password.")

    if conn:
        conn.close()
    return st.session_state.get("logged_in", False)

def register_ui(conn=None):
    if conn is None:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    
    st.subheader("Register")
    display_name = st.text_input("Full name")
    username = st.text_input("Username", key="reg_username").strip().lower()
    email = st.text_input("Email", key="reg_email").strip().lower()
    password = st.text_input("Password", type="password", key="reg_password")
    confirm_pw = st.text_input("Confirm Password", type="password", key="reg_confirm")

    if st.button("Create Account"):
        EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(EMAIL_PATTERN, email):
            st.error("Invalid email")
            return
        if password != confirm_pw:
            st.error("Passwords don't match")
            return
        if not display_name or not username:
            st.error("Name and username required")
            return

        if create_user(conn, username, display_name, email, password):
            st.success("Account created! Please login.")
        else:
            st.error("Username/email exists")

    if conn:
        conn.close()

def require_login():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("Please log in")
        st.stop()

def current_user():
    return st.session_state.get("user", None)

def profile_page(conn=None):
    require_login()
    user = current_user()
    st.header(f"Profile: {user['display_name']}")
    st.write(f"**Username:** {user['username']}")
    st.write(f"**Email:** {user['email']}")

    with st.expander("Change Password"):
        old_pw = st.text_input("Old password", type="password")
        new_pw = st.text_input("New password", type="password")
        confirm_pw = st.text_input("Confirm", type="password")
        if st.button("Update"):
            if conn is None:
                conn = sqlite3.connect(DB_PATH, check_same_thread=False)
            db_user = get_user_by_username(conn, user["username"])
            if not check_password_hash(db_user["password_hash"], old_pw):
                st.error("Wrong old password")
            elif new_pw != confirm_pw:
                st.error("Passwords don't match")
            else:
                new_hash = generate_password_hash(new_pw)
                c = conn.cursor()
                c.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user["id"]))
                conn.commit()
                st.success("Password updated!")
            if conn and not hasattr(conn, '_autocommit'):
                conn.close()

def google_login_button():
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    if not GOOGLE_CLIENT_ID:
        st.info("Google login: Add GOOGLE_CLIENT_ID to .env")
        return
    
    public_url = os.getenv("PUBLIC_URL", "http://localhost:8501")
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={GOOGLE_CLIENT_ID}&redirect_uri={public_url}&response_type=code&scope=openid%20email%20profile"
    st.markdown(f'''
        <style>
        .gbtn{{
            background: linear-gradient(135deg, #FFD54F 0%, #FFC107 50%, #FF9800 100%);
            color: #5D4037 !important;
            border: none !important;
            padding: 12px;
            border-radius: 8px;
            font-weight: 600;
            width: 100%;
            box-shadow: 0 4px 14px rgba(255, 193, 7, 0.4);
            transition: all 0.3s ease;
        }}
        .gbtn:hover{{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 193, 7, 0.6);
            background: linear-gradient(135deg, #FFEB3B 0%, #FFD54F 50%, #FFC107 100%);
        }}
        </style>
        <a href="{auth_url}" target="_self" style="text-decoration:none;display:block;">
            <button class="gbtn">👤 Google Login</button>
        </a>
    ''', unsafe_allow_html=True)

