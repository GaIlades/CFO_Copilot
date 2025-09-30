import streamlit as st
from agent.tools import FinanceTools
from agent.planner import CFOPlanner

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
# Initialize tools and planner
# ----------------------
@st.cache_resource
def init_agent():
    tools = FinanceTools()
    planner = CFOPlanner(tools)
    return tools, planner

try:
    tools, planner = init_agent()
    data_loaded = True
except Exception as e:
    st.error(f"Error loading data: {e}")
    data_loaded = False
    tools = None
    planner = None

# ----------------------
# Header
# ----------------------
st.title("💰 CFO Copilot")
st.markdown("Ask me anything about your financials!")

# ----------------------
# Sidebar
# ----------------------
if data_loaded:
    st.sidebar.header("Data Overview")
    data_summary = tools.get_data_summary()
    
    for dataset, info in data_summary.items():
        st.sidebar.write(f"**{dataset.title()}**: {info['rows']} rows")

    st.sidebar.header("Sample Questions")
    sample_questions = [
        "What was February 2024 revenue vs budget in USD?",
        "Show revenue vs budget for all months",
        "Show gross margin % trend for last 3 months",
        "What is our gross margin?"
    ]

    for question in sample_questions:
        if st.sidebar.button(question, key=f"sample_{hash(question)}"):
            st.session_state.messages.append({"role": "user", "content": question})
            
            response = planner.answer_question(question)
            st.session_state.messages.append({
                "role": "assistant",
                "content": response["text"],
                "chart": response.get("chart")
            })

else:
    st.sidebar.error("Data not loaded")

# ----------------------
# Chat messages
# ----------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("chart"):
            st.plotly_chart(message["chart"], use_container_width=True)

# ----------------------
# Chat input
# ----------------------
if prompt := st.chat_input("Ask about your financials..."):
    if not data_loaded:
        st.error("Cannot process questions - data not loaded")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                response = planner.answer_question(prompt)
                st.markdown(response["text"])
                
                if response.get("chart"):
                    st.plotly_chart(response["chart"], use_container_width=True)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["text"],
                    "chart": response.get("chart")
                })