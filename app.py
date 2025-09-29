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

try:
    tools = init_tools()
    data_loaded = True
except Exception as e:
    st.error(f"Error loading data: {e}")
    data_loaded = False
    tools = None

# ----------------------
# Header
# ----------------------
st.title("💰 CFO Copilot")
st.markdown("Ask me anything about your financials!")

# ----------------------
# Helper: generate response
# ----------------------
def generate_response(prompt: str) -> str:
    """Generate assistant response given a user prompt."""
    if not data_loaded:
        return "Error loading CSV files."

    prompt_lower = prompt.lower()
    #revenue
    if "revenue" in prompt_lower:
        result = tools.get_revenue_summary()
        if "error" in result:
            return f" {result['error']}"
        else:
            response = f"**Revenue Summary:**\n\n"
            response += f" Total Revenue: ${result['total_revenue_usd']:,.2f} USD\n"
            response += f" Months covered: {', '.join(result['months'])}\n"
            response += f" Entities: {', '.join(result['entities'])}\n"
            response += f" Records: {result['records']}"
            return response
    #data summary
    elif "data" in prompt_lower:
        data_summary = tools.get_data_summary()
        response = f" **Data Summary:**\n\n"
        for dataset, info in data_summary.items():
            response += f" **{dataset.title()}**: {info['rows']} rows\n"
        return response

    else:
        response = f"I understand you asked: '{prompt}'\n\n"
        response += "I can help with:\n"
        response += "Revenue analysis (try 'show revenue summary')\n"
        response += "Data overview (try 'what data do we have')"
        return response

# ----------------------
# Sidebar with data info
# ----------------------
if data_loaded:
    st.sidebar.header("Data Overview")
    data_summary = tools.get_data_summary()

    for dataset, info in data_summary.items():
        st.sidebar.write(f"**{dataset.title()}**: {info['rows']} rows")

    st.sidebar.header("Try asking:")
    sample_questions = [
        "Show me revenue summary",
        "What data do we have?"
    ]

    for question in sample_questions:
        if st.sidebar.button(question, key=f"sample_{hash(question)}"):
            st.session_state.messages.append({"role": "user", "content": question})
            response = generate_response(question)
            st.session_state.messages.append({"role": "assistant", "content": response})

else:
    st.sidebar.error("Data not loaded")

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
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = generate_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)