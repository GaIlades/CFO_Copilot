# CFO Copilot 💰

A financial analysis assistant that helps CFOs quickly analyze monthly financials through natural language questions and interactive visualizations.

## Overview

This application generates charts and displays financial data based on queries about revenue, gross margin, operating expenses, EBITDA, and cash runway. It processes CSV financial data and provides instant answers with supporting visualizations.

## Quick Start

### Installation

Clone this repository:
```bash
git clone https://github.com/GaIlades/CFO_Copilot.git
cd CFO_Copilot
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the application:
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## Usage

### Sample Questions

The application can answer questions like:
- "What was February 2024 revenue vs budget in USD?"
- "Show gross margin % trend for last 3 months"
- "Break down Opex by category for February 2024"
- "What is our EBITDA for February 2024?"
- "What is our cash runway right now?"

Sample questions are provided in the sidebar for quick access.

### Export PDF Report

Click the "📄 Export Summary PDF" button in the sidebar to generate a comprehensive financial summary report including:
- Revenue vs Budget analysis with charts
- Operating Expenses breakdown with pie chart
- Cash Runway analysis

## Features

- **Revenue Analysis**: Actual vs budget comparison with variance tracking
- **Gross Margin Trends**: Calculate and visualize (Revenue - COGS) / Revenue over time
- **OpEx Breakdown**: Operating expenses grouped by category
- **EBITDA Calculation**: Revenue - COGS - OpEx analysis
- **Cash Runway**: Months of runway based on current cash and average burn rate (last 3 months)
- **Multi-currency Support**: Automatic USD conversion using FX rates
- **Interactive Charts**: Plotly-powered visualizations

## Data Structure

The application reads from CSV files in the `fixtures/` directory:
- `actuals.csv` - Monthly actual financial data
- `budget.csv` - Monthly budgeted amounts
- `cash.csv` - Monthly cash balances
- `fx.csv` - Currency exchange rates for USD conversion

## Testing

Run the test suite using PyTest:
```bash
pytest test/test_agent.py -v
```

Tests validate:
- Revenue vs budget variance calculations
- Gross margin percentage formulas
- Cash runway computation logic

## Project Structure

```
CFO_Copilot/
├── app.py                # Streamlit web interface
├── agent/
│   ├── tools.py          # Financial calculation functions
│   └── planner.py        # Query classification and routing
├── fixtures/             # CSV data files
│   ├── actuals.csv
│   ├── budget.csv
│   ├── cash.csv
│   └── fx.csv
├── test/
│   └── test_agent.py     # Unit tests
├── requirements.txt      # Python dependencies
└── README.md
```

## Architecture

This agent uses **rule-based keyword matching** for query classification. This approach provides:
- Fast, deterministic responses
- No external API dependencies or costs
- Easy debugging and testing
- Reliable handling of predefined question patterns

## License

MIT