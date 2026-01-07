import streamlit as st

# def navbar():
#     st.markdown("""
#         <style>
#         .navbar {display: flex; gap: 30px;}
#         .navbar a {font-size: 20px; text-decoration: none; color: #2980b9;}
#         .username {font-weight: bold; color: #20b34b;}
#         </style>
#         """, unsafe_allow_html=True)
#     st.markdown('<div class="navbar">'
#                 '<a href="/Home" target="_self">Home</a> '
#                 '<a href="/login-signup" target="_self">Logout</a> '
#                 '<span class="username"> ' + st.session_state.get("email", "") + '</span>'
#                 '</div>', unsafe_allow_html=True)

st.set_page_config(page_title="Generate Documentation | MACDG", layout="wide")

if not st.session_state.get("jwt"):
    st.warning("Please login to access this page!")
    st.stop()

# navbar()

last_project_id = st.session_state.get("last_project_id")
if not last_project_id:
    st.info("No project selected. Please clone a repo first.")
    st.stop()

st.title("Documentation Generation")
st.write(f"Project ID: `{last_project_id}`")

if st.button("Generate Documentation"):
    st.success("Documentation generation triggered! (implement backend call here)")
