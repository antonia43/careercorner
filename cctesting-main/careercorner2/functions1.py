
import pandas as pd
import streamlit as st
import requests
import os
from urllib.parse import urlencode



def load_zip_data():
    df = pd.read_csv("/Users/antonialemos/Desktop/testing proj/CP7_Portugal_nov2022.txt",
        sep="\t",
        names=["zip", "city", "lat", "lon"],
        dtype=str,
        low_memory=False
        )
    # Swap lat/lon because the dataset stores them reversed
    df = df.rename(columns={"lat": "lon", "lon": "lat"})

    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
    df = df.dropna(subset=["lat", "lon"])
    df = df[(df["lat"].between(36, 43)) & (df["lon"].between(-10, -6))]
    return df


@st.cache_data
def get_companies_overpass(lat, lon, radius_meters, sector):
    try:
        api = overpass.API(timeout=60)
        query = f"""
        [out:json];
        (
          node["name"](around:{radius_meters},{lat},{lon});
          way["name"](around:{radius_meters},{lat},{lon});
          relation["name"](around:{radius_meters},{lat},{lon});
        );
        out center;
        """

        response = api.get(query)

        companies = []
        for element in response.get("features", []):
            name = element["properties"].get("name", "")
            if sector.lower() in name.lower():
                coords = element["geometry"]["coordinates"]
                lon, lat = coords  # GeoJSON uses lon, lat order
                companies.append({
                    "name": name,
                    "lat": lat,
                    "lon": lon,
                    "category": sector
                })

        return companies

    except Exception as e:
        st.error(f"Error fetching company data: {e}")
        return []
    
    
@st.cache_data
def test_all_companies_portugal():
    """Fetch companies around central Portugal to test Overpass via HTTP."""
    lat, lon = 39.5, -8.0
    radius_meters = 50000

    st.info("Fetching companies in a 50 km radius around central Portugal… please wait up to 30 s.")

    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    (
      node["name"](around:{radius_meters},{lat},{lon});
      way["name"](around:{radius_meters},{lat},{lon});
      relation["name"](around:{radius_meters},{lat},{lon});
    );
    out center;
    """

    try:
        response = requests.get(overpass_url, params={"data": query}, timeout=60)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        st.error(f"Error fetching test data: {e}")
        return []

    companies = []
    for element in data.get("elements", []):
        name = element.get("tags", {}).get("name")
        if not name:
            continue

        if "lat" in element and "lon" in element:
            lat, lon = element["lat"], element["lon"]
        elif "center" in element:  # ways/relations
            lat, lon = element["center"]["lat"], element["center"]["lon"]
        else:
            continue

        companies.append({"name": name, "lat": lat, "lon": lon})

    st.success(f"Retrieved {len(companies)} companies.")
    return companies


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
