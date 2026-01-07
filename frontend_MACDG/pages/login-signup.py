import streamlit as st
import requests

st.set_page_config(page_title="Login / Signup | MACDG", layout="wide")
st.title("Welcome to Multi-Agent Code Doc Platform")

tab = st.radio("Choose action:", ["Login", "Sign Up"])

email = st.text_input("Email")
password = st.text_input("Password", type="password")
role = st.selectbox("Role", ["User", "Admin"]) if tab == "Sign Up" else None

if st.button(tab):
    url = "http://localhost:8000/auth/signup" if tab == "Sign Up" else "http://localhost:8000/auth/login"
    payload = {"email": email, "password": password}
    if tab == "Sign Up":
        payload["role"] = role
    resp = requests.post(url, json=payload)
    if resp.ok:
        st.success(f"{tab} successful!")
        access_token = resp.json()['access_token']
        st.session_state['jwt'] = access_token
        st.session_state['email'] = email
        st.session_state['role'] = role if tab == "Sign Up" else "User"
        # st.experimental_rerun()
    else:
        st.error(resp.json().get('detail', 'Authentication failed'))
        
if st.session_state.get('jwt'):
    st.info("You are logged in.")
    # st.markdown("[Go to Home](/)")
