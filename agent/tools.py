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
            return pd.DataFrame()  # Return an empty DataFrame on error

    def load_budget(self):
        try: 
            path = os.path.join(self.fixtures_dir, 'budget.csv')
            df = pd.read_csv(path)
            print(f"Loaded budget: {len(df)} rows") 
            return df
        except Exception as e:
            print(f"Error loading budget: {e}")
            return pd.DataFrame()  # Return an empty DataFrame on error
        
    def load_cash(self):
        try: 
            path = os.path.join(self.fixtures_dir, 'cash.csv')
            df = pd.read_csv(path)
            print(f"Loaded cash: {len(df)} rows") 
            return df
        except Exception as e:
            print(f"Error loading cash: {e}")
            return pd.DataFrame()  # Return an empty DataFrame on error
        
    def load_fx(self):
        try: 
            path = os.path.join(self.fixtures_dir, 'fx.csv')
            df = pd.read_csv(path)
            print(f"Loaded fx: {len(df)} rows") 
            return df
        except Exception as e:
            print(f"Error loading fx: {e}")
            return pd.DataFrame()  # Return an empty DataFrame on error

    def get_data_summary(self):
        summary = {
            "actuals": {"rows": len(self.actuals), "columns": self.actuals.columns.tolist() if not self.actuals.empty else []},
            "budget": {"rows": len(self.budget), "columns": self.budget.columns.tolist() if not self.budget.empty else []},
            "cash": {"rows": len(self.cash), "columns": self.cash.columns.tolist() if not self.cash.empty else []},
            "fx": {"rows": len(self.fx), "columns": self.fx.columns.tolist() if not self.fx.empty else []},
        }
        return summary
