import streamlit as st
from agent.tools import FinanceTools

# ----------------------
# Page config
# ----------------------
st.set_page_config(
    page_title="CFO Copilot",
    page_icon="💰",
    layout="wide"
)

# ----------------------
# Initialize session state
# ----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------
# Initialize tools (with caching)
# ----------------------
@st.cache_resource
def init_tools():
    return FinanceTools()

tools = init_tools()

# ----------------------
# Helper: generate response
# ----------------------
def generate_response(prompt: str):
    """Generate a response based on user prompt."""
    data_summary = tools.get_data_summary()

    if "data" in prompt.lower() or "show" in prompt.lower():
        if "actuals" in prompt.lower():
            if not tools.actuals.empty:
                response = f"**Actuals Data Overview:**\n\n"
                response += f"• Total records: {len(tools.actuals)}\n"
                response += f"• Columns: {', '.join(tools.actuals.columns)}\n\n"
                response += f"**Sample data:**\n{tools.actuals.head().to_string()}"
            else:
                response = "No actuals data found."
        else:
            response = f"**Data Summary:**\n\n"
            for dataset, info in data_summary.items():
                response += f"• {dataset.title()}: {info['rows']} rows\n"
    else:
        response = f"I understand you asked: '{prompt}'\n\nI'm still learning! Try asking about 'data' or 'actuals' for now."

    return response

# ----------------------
# Header
# ----------------------
st.title("💰 CFO Copilot")
st.markdown("Ask me anything about your financials!")

# ----------------------
# Sidebar with data info
# ----------------------
st.sidebar.header("Data Overview")
data_summary = tools.get_data_summary()

for dataset, info in data_summary.items():
    st.sidebar.write(f"**{dataset.title()}**: {info['rows']} rows")

# Add a debug expander
with st.sidebar.expander("Debug Info"):
    st.json(data_summary)

# ----------------------
# Sample questions in sidebar
# ----------------------
st.sidebar.header("Try asking:")
sample_questions = [
    "Show me the actuals data",
    "What data do we have?",
    "Display revenue information"
]

for question in sample_questions:
    if st.sidebar.button(question, key=f"sample_{hash(question)}"):
        # Save user message
        st.session_state.messages.append({"role": "user", "content": question})

        # Generate and save assistant response
        response = generate_response(question)
        st.session_state.messages.append({"role": "assistant", "content": response})

# ----------------------
# Messaging
# ----------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----------------------
# User input
# ----------------------
if prompt := st.chat_input("Ask about your financials..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and save assistant response
    response = generate_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
