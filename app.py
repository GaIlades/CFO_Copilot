import streamlit as st

# ----------------------
# Page config
# ----------------------
st.set_page_config(
    page_title="CFO Copilot",
    page_icon="💰",
    layout="wide"
)

# ----------------------
# Sidebar
# ----------------------
st.sidebar.title("Sidebar")
page = st.sidebar.radio("Navigation", ["Home"])

# ----------------------
# Main content
# ----------------------
if page == "Home":
    st.title("Hi")
    st.write("Hello World!")

