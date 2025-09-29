import pandas as pd
import os
import plotly.graph_objects as go

class FinanceTools:
    def __init__(self, fixtures_dir='fixtures'):
        self.fixtures_dir = fixtures_dir
        self.actuals = self.load_actuals()
        self.budget = self.load_budget()
        self.cash = self.load_cash()
        self.fx = self.load_fx()

    def load_actuals(self):
        try: 
            path = os.path.join(self.fixtures_dir, 'actuals.csv')
            df = pd.read_csv(path)
            print(f"Loaded actuals: {len(df)} rows")
            return df
        except Exception as e:
            print(f"Error loading actuals: {e}")
            return pd.DataFrame()

    def load_budget(self):
        try: 
            path = os.path.join(self.fixtures_dir, 'budget.csv')
            df = pd.read_csv(path)
            print(f"Loaded budget: {len(df)} rows")
            return df
        except Exception as e:
            print(f"Error loading budget: {e}")
            return pd.DataFrame()
        
    def load_cash(self):
        try: 
            path = os.path.join(self.fixtures_dir, 'cash.csv')
            df = pd.read_csv(path)
            print(f"Loaded cash: {len(df)} rows")
            return df
        except Exception as e:
            print(f"Error loading cash: {e}")
            return pd.DataFrame()
        
    def load_fx(self):
        try: 
            path = os.path.join(self.fixtures_dir, 'fx.csv')
            df = pd.read_csv(path)
            print(f"Loaded fx: {len(df)} rows")
            return df
        except Exception as e:
            print(f"Error loading fx: {e}")
            return pd.DataFrame()
        
    def convert_to_usd(self, df, amount_col='amount'):
        """Convert amounts to USD using FX rates"""
        if self.fx.empty:
            print("No FX data available")
            df = df.copy()
            df[f'{amount_col}_usd'] = df[amount_col]    
            return df
        
        df_with_fx = df.merge(self.fx, on=['month', 'currency'], how='left')
        df_with_fx['rate_to_usd'] = df_with_fx['rate_to_usd'].fillna(1.0)
        df_with_fx[f'{amount_col}_usd'] = df_with_fx[amount_col] * df_with_fx['rate_to_usd']
        
        return df_with_fx

    def get_revenue_vs_budget(self, month=None):
        """Get revenue vs budget comparison"""
        if self.actuals.empty or self.budget.empty:
            return pd.DataFrame()
        
        actuals_rev = self.actuals[self.actuals['account_category'].str.contains('Revenue', case=False, na=False)].copy()
        budget_rev = self.budget[self.budget['account_category'].str.contains('Revenue', case=False, na=False)].copy()
        
        if actuals_rev.empty or budget_rev.empty:
            return pd.DataFrame()
        
        actuals_usd = self.convert_to_usd(actuals_rev)
        budget_usd = self.convert_to_usd(budget_rev)
        
        if month:
            actuals_usd = actuals_usd[actuals_usd['month'] == month]
            budget_usd = budget_usd[budget_usd['month'] == month]
        
        actuals_agg = actuals_usd.groupby('month')['amount_usd'].sum().reset_index()
        budget_agg = budget_usd.groupby('month')['amount_usd'].sum().reset_index()
        
        comparison = actuals_agg.merge(budget_agg, on='month', suffixes=('_actual', '_budget'))
        comparison['variance'] = comparison['amount_usd_actual'] - comparison['amount_usd_budget']
        comparison['variance_pct'] = (comparison['variance'] / comparison['amount_usd_budget']) * 100
        
        return comparison

    def create_revenue_chart(self, data):
        """Create revenue vs budget chart"""
        if data.empty:
            return None
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=data['month'],
            y=data['amount_usd_actual'],
            name='Actual',
            marker_color='#2E86AB'
        ))
        
        fig.add_trace(go.Bar(
            x=data['month'],
            y=data['amount_usd_budget'],
            name='Budget',
            marker_color='#A23B72'
        ))
        
        fig.update_layout(
            title='Revenue: Actual vs Budget',
            xaxis_title='Month',
            yaxis_title='Amount (USD)',
            barmode='group',
            template='plotly_white',
            height=400
        )
        
        return fig

    def get_data_summary(self):
        """Get summary of all loaded data"""
        summary = {
            "actuals": {"rows": len(self.actuals), "columns": self.actuals.columns.tolist() if not self.actuals.empty else []},
            "budget": {"rows": len(self.budget), "columns": self.budget.columns.tolist() if not self.budget.empty else []},
            "cash": {"rows": len(self.cash), "columns": self.cash.columns.tolist() if not self.cash.empty else []},
            "fx": {"rows": len(self.fx), "columns": self.fx.columns.tolist() if not self.fx.empty else []},
        }
        return summary