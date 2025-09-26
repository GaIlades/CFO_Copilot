import streamlit as st

# ----------------------
# Page config
# ----------------------
st.set_page_config(
    page_title="CFO Copilot",
    page_icon="$",
    layout="wide"
)

# ----------------------
# Initialize session state
# ----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------
# Sidebar
# ----------------------
st.sidebar.title("Sidebar")
page = st.sidebar.radio("Navigation", ["Home"])

# ----------------------
# Messaging
# ----------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ----------------------
# User input
# ----------------------
if prompt := st.chat_input("Type something..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    response = f"You have typed: {prompt}"

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)