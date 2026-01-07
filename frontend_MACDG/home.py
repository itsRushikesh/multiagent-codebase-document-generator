import streamlit as st
import requests

st.set_page_config(page_title="Home | MACDG", layout="wide")

# def navbar():
#     st.markdown("""
#         <style>
#         .navbar {display: flex; gap: 28px; padding-bottom: 0.5rem;}
#         .navbar a {font-size: 18px; text-decoration: none; color: #2E60A7;}
#         .username {font-weight: bold; color: #208040;}
#         </style>
#         """, unsafe_allow_html=True)
#     login_status = (
#         f'<span class="username">{st.session_state.get("email")}</span> '
#         '<a href="?page=login-signup">(Logout)</a>'
#         if st.session_state.get("jwt")
#         else '<a href="login-signup">Login / Signup</a>'
#     )
#     st.markdown(
#         '<div class="navbar">'
#         # '<a href="/">Home</a> '
#         f'{login_status}</div>',
#         unsafe_allow_html=True
#     )

# navbar()
st.title("Project Dashboard")

st.header("Your Projects")
if st.button("List My Projects"):
    if not st.session_state.get("jwt"):
        st.warning("Please login to list your projects.")
        if st.button("Go to Login/Signup"):
            st.experimental_set_query_params(page="login-signup")
            st.experimental_rerun()
    else:
        headers = {'Authorization': f'Bearer {st.session_state["jwt"]}'}
        resp = requests.get("http://localhost:8000/project/list-projects", headers=headers)
        if resp.ok:
            projects = resp.json()
            if projects:
                for p in projects:
                    st.write(f"• {p['id']} - {p['repo_url']}")
            else:
                st.info("You don't have any projects yet.")
        else:
            st.error("Failed to fetch projects.")

# Add New Project UI
st.header("Add New Project")
repo_url = st.text_input("GitHub Repository URL")
personas = st.multiselect("Select personas for docs:", ["SDE", "PM"])

if st.button("Clone Repository and Initiate Project"):
    if not st.session_state.get("jwt"):
        st.warning("Please login to upload/clone a repo first.")
        if st.button("Go to Login/Signup", key="login-upload"):
            st.experimental_set_query_params(page="login-signup")
            st.experimental_rerun()
    elif not repo_url or not personas:
        st.warning("Please provide both URL and personas")
    else:
        with st.spinner("Cloning repository... this may take a few seconds."):
            headers = {'Authorization': f'Bearer {st.session_state["jwt"]}'}
            payload = {
                "repo_url": repo_url,
                "personas": personas
            }
            resp = requests.post("http://localhost:8000/project/initiate-project", json=payload, headers=headers)
            if resp.ok:
                st.success("Repository cloned successfully! Ready to generate documentation.")
                st.session_state["last_project_id"] = resp.json()["project_id"]
                st.session_state["last_personas"] = personas
                st.markdown('[Go to Generate Documentation](./Generate-Doc)')
            else:
                st.error(resp.json().get("detail", "Clone failed!"))

# Optionally show proceed to doc generation if repo was just cloned
if st.session_state.get("last_project_id") and st.session_state.get("jwt"):
    if st.button("Proceed to Generate Documentation"):
        st.switch_page("Generate-Doc")  # Use if you have streamlit-extras, else use a link.

