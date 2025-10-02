import streamlit as st
from agent.tools import FinanceTools
from agent.planner import CFOPlanner
from datetime import datetime
import os
import tempfile

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
# Export Summary PDF Function
# ----------------------
def export_summary_pdf():
    """Export key financial metrics: Revenue vs Budget, Opex Breakdown, Cash Runway"""
    from fpdf import FPDF
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 15, "CFO Financial Summary Report", ln=True, align='C')
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
    pdf.ln(10)
    
    # 1. Revenue vs Budget
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Revenue vs Budget", ln=True)
    pdf.set_font("Arial", '', 11)
    
    rev_data = tools.get_revenue_vs_budget()
    if not rev_data.empty:
        total_actual = rev_data['amount_usd_actual'].sum()
        total_budget = rev_data['amount_usd_budget'].sum()
        variance = total_actual - total_budget
        variance_pct = (variance / total_budget) * 100
        
        pdf.cell(0, 8, f"Total Actual: ${total_actual:,.0f}", ln=True)
        pdf.cell(0, 8, f"Total Budget: ${total_budget:,.0f}", ln=True)
        pdf.cell(0, 8, f"Variance: ${variance:,.0f} ({variance_pct:.1f}%)", ln=True)
        pdf.ln(5)
        
        # Add chart
        chart = tools.create_revenue_chart(rev_data)
        if chart:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                img_bytes = chart.to_image(format="png", width=800, height=400)
                tmpfile.write(img_bytes)
                tmpfile_path = tmpfile.name
            pdf.image(tmpfile_path, x=10, w=190)
            os.remove(tmpfile_path)
    else:
        pdf.cell(0, 8, "No revenue data available", ln=True)
    
    pdf.ln(10)
    
    # 2. Opex Breakdown
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Operating Expenses Breakdown", ln=True)
    pdf.set_font("Arial", '', 11)
    
    opex_data = tools.get_opex_breakdown()
    if not opex_data.empty:
        total_opex = opex_data['amount_usd'].sum()
        pdf.cell(0, 8, f"Total OpEx: ${total_opex:,.0f}", ln=True)
        pdf.ln(5)
        
        for _, row in opex_data.iterrows():
            pct = (row['amount_usd'] / total_opex) * 100
            pdf.cell(0, 8, f"{row['category']}: ${row['amount_usd']:,.0f} ({pct:.1f}%)", ln=True)
        
        pdf.ln(5)
        
        # Add chart
        chart = tools.create_opex_chart(opex_data)
        if chart:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                img_bytes = chart.to_image(format="png", width=800, height=400)
                tmpfile.write(img_bytes)
                tmpfile_path = tmpfile.name
            pdf.image(tmpfile_path, x=10, w=190)
            os.remove(tmpfile_path)
    else:
        pdf.cell(0, 8, "No OpEx data available", ln=True)
    
    pdf.ln(10)
    
    # 3. Cash Runway
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Cash Runway Analysis", ln=True)
    pdf.set_font("Arial", '', 11)
    
    runway_data = tools.calculate_cash_runway()
    if "error" not in runway_data:
        pdf.cell(0, 8, f"Current Cash: ${runway_data['current_cash']:,.0f}", ln=True)
        pdf.cell(0, 8, f"Avg Monthly Burn: ${runway_data['avg_monthly_burn']:,.0f}", ln=True)
        
        if runway_data['runway_months'] == float('inf'):
            pdf.cell(0, 8, "Runway: Cash positive (no burn)", ln=True)
        else:
            pdf.cell(0, 8, f"Runway: {runway_data['runway_months']:.1f} months", ln=True)
    else:
        pdf.cell(0, 8, runway_data["error"], ln=True)
    
    return pdf.output(dest='S').encode('latin1')

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
        "Show gross margin % trend for last 3 months",
        "Break down Opex by category for February 2024",
        "What is our EBITDA for February 2024?",
        "What is our cash runway right now?"
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

    # Export PDF Button
    st.sidebar.markdown("---")
    st.sidebar.header("Export Report")
    
    if st.sidebar.button("📄 Export Summary PDF"):
        try:
            with st.spinner("Generating summary report..."):
                pdf_bytes = export_summary_pdf()
                st.sidebar.download_button(
                    label="⬇️ Download PDF",
                    data=pdf_bytes,
                    file_name="CFO_Summary_Report.pdf",
                    mime="application/pdf"
                )
                st.sidebar.success("Summary report ready!")
        except Exception as e:
            st.sidebar.error(f"Error: {str(e)}")

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