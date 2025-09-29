import pandas as pd
import os 

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
            print(f"Columns: {df.columns.tolist()}")
            print(f"Sample data:\n{df.head()}")
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
        
        # Merge with FX data
        df_with_fx = df.merge(self.fx, on=['month', 'currency'], how='left')
        
        # Handle missing FX rates (assume 1.0 for USD or missing rates)
        df_with_fx['rate_to_usd'] = df_with_fx['rate_to_usd'].fillna(1.0)
        df_with_fx[f'{amount_col}_usd'] = df_with_fx[amount_col] * df_with_fx['rate_to_usd']
        
        return df_with_fx

    def get_revenue_summary(self, month=None):
        """Get revenue summary with proper variable scoping"""
        if self.actuals.empty:
            return {"error": "No actuals data available"}
        
        # Filter for revenue data - FIXED: Define revenue_data properly
        revenue_data = self.actuals[self.actuals['account_category'].str.contains("Revenue", case=False, na=False)].copy()
        
        if revenue_data.empty:
            return {"error": "No revenue data found in actuals"}
        
        # Filter by month if specified
        if month:
            revenue_data = revenue_data[revenue_data['month'] == month]
            if revenue_data.empty:
                return {"error": f"No revenue data found for month: {month}"}
        
        # Convert to USD
        revenue_usd = self.convert_to_usd(revenue_data)

        total_revenue = revenue_usd['amount_usd'].sum()
        months = sorted(revenue_usd['month'].unique())
        entities = sorted(revenue_usd['entity'].unique())

        return {
            "total_revenue_usd": total_revenue,
            "months": months,
            "entities": entities,
            "records": len(revenue_usd)
        }

    def get_data_summary(self):
        """Get summary of all loaded data"""
        summary = {
            "actuals": {"rows": len(self.actuals), "columns": self.actuals.columns.tolist() if not self.actuals.empty else []},
            "budget": {"rows": len(self.budget), "columns": self.budget.columns.tolist() if not self.budget.empty else []},
            "cash": {"rows": len(self.cash), "columns": self.cash.columns.tolist() if not self.cash.empty else []},
            "fx": {"rows": len(self.fx), "columns": self.fx.columns.tolist() if not self.fx.empty else []},
        }
        return summary