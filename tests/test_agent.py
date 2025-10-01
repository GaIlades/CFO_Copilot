import pytest
import pandas as pd
from agent.tools import FinanceTools

@pytest.fixture
def tools():
    # Fixture to initialize FinanceTools with test data
    return FinanceTools(fixtures_dir='fixtures')

def test_revenue_vs_budget_calculation(tools):
    # Test that revenue vs budget calculates variance correctly
    # Get revenue data for a specific month
    data = tools.get_revenue_vs_budget(month='2024-02')
    
    # Verify data is not empty
    assert not data.empty, "Revenue data should not be empty"
    
    # Verify required columns exist
    assert 'amount_usd_actual' in data.columns
    assert 'amount_usd_budget' in data.columns
    assert 'variance' in data.columns
    assert 'variance_pct' in data.columns
    
    # Verify variance calculation is correct
    row = data.iloc[0]
    expected_variance = row['amount_usd_actual'] - row['amount_usd_budget']
    assert abs(row['variance'] - expected_variance) < 0.01, "Variance calculation should be correct"
    
    # Verify variance percentage is correct
    expected_pct = (row['variance'] / row['amount_usd_budget']) * 100
    assert abs(row['variance_pct'] - expected_pct) < 0.01, "Variance percentage should be correct"

def test_gross_margin_calculation(tools):
    # Test that gross margin percentage is calculated correctly
    data = tools.get_gross_margin_trend()
    
    # Verify data is not empty
    assert not data.empty, "Margin data should not be empty"
    
    # Verify required columns exist
    assert 'revenue' in data.columns
    assert 'cogs' in data.columns
    assert 'gross_margin' in data.columns
    assert 'gross_margin_pct' in data.columns
    
    # Verify margin calculation for first row
    row = data.iloc[0]
    expected_margin = row['revenue'] - row['cogs']
    expected_pct = (expected_margin / row['revenue']) * 100
    
    assert abs(row['gross_margin'] - expected_margin) < 0.01, "Gross margin should be revenue - cogs"
    assert abs(row['gross_margin_pct'] - expected_pct) < 0.01, "Gross margin % should be correct"

def test_cash_runway_calculation(tools):
    # Test that cash runway returns valid data structure
    runway_data = tools.calculate_cash_runway()
    
    # Verify no errors
    assert "error" not in runway_data, "Cash runway should not return an error"
    
    # Verify required keys exist
    assert 'current_cash' in runway_data
    assert 'avg_monthly_burn' in runway_data
    assert 'runway_months' in runway_data
    
    # Verify values are positive numbers
    assert runway_data['current_cash'] > 0, "Current cash should be positive"
    assert runway_data['avg_monthly_burn'] >= 0, "Average burn should be non-negative"
    
    # Verify runway calculation
    if runway_data['avg_monthly_burn'] > 0:
        expected_runway = runway_data['current_cash'] / runway_data['avg_monthly_burn']
        assert abs(runway_data['runway_months'] - expected_runway) < 0.01, "Runway calculation should be correct"