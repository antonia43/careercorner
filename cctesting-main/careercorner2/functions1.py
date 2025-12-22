
import pandas as pd
import streamlit as st
import requests
import os
from urllib.parse import urlencode

# Reset function: go back to main welcome screen
def reset():
    st.session_state.user_type = None

def google_login_button():
    """
    Renders a Google OAuth login button that redirects to Google's OAuth consent screen
    """
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    # Local dev default; on deploy set REDIRECT_URI in your secrets to your public URL
    REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8501")

    google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"

    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }

    auth_url = f"{google_auth_url}?{urlencode(params)}"

    st.markdown(
        f"""
        <style>
        .google-signin-button {{
            display: inline-block;
            width: 100%;
            text-decoration: none;
        }}
        .google-signin-button button {{
            background-color: #FFEB3B !important;
            color: #33691E !important;
            padding: 12px 20px;
            border: 2px solid #FDD835 !important;
            border-radius: 15px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
            font-weight: 600;
            font-family: 'Quicksand', sans-serif;
            transition: all 0.3s ease;
            box-shadow: 0 3px 10px rgba(253, 216, 53, 0.3);
        }}
        .google-signin-button button:hover {{
            background-color: #FFF176 !important;
            border-color: #FFEB3B !important;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(253, 216, 53, 0.5);
        }}
        </style>
        <a href="{auth_url}" target="_self" class="google-signin-button">
            <button>
                Sign in with Google
            </button>
        </a>
        """,
        unsafe_allow_html=True,
    )
