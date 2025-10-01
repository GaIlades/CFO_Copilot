import re

class CFOPlanner:
    def __init__(self, tools):
        self.tools = tools
    
    def extract_month(self, question):
        """Extract month from question like 'February 2024' -> '2024-02'"""
        month_names = {
            'january': '01', 'february': '02', 'march': '03', 'april': '04',
            'may': '05', 'june': '06', 'july': '07', 'august': '08',
            'september': '09', 'october': '10', 'november': '11', 'december': '12'
        }
        
        # Pattern: "February 2024"
        match = re.search(r'(\w+)\s+(\d{4})', question.lower())
        if match:
            month_name, year = match.groups()
            if month_name in month_names:
                return f"{year}-{month_names[month_name]}"
        
        return None
    
    def extract_months_count(self, question):
        """Extract number of months from question like 'last 3 months' -> 3"""
        match = re.search(r'last\s+(\d+)\s+months?', question.lower())
        if match:
            return int(match.group(1))
        return None
    
    def answer_question(self, question):
        """Answer financial questions"""
        question_lower = question.lower()
        
        # OpEx Breakdown
        if 'opex' in question_lower or 'operating expense' in question_lower or 'breakdown' in question_lower:
            month = self.extract_month(question)
            data = self.tools.get_opex_breakdown(month)
            
            if data.empty:
                return {"text": "No operating expense data found.", "chart": None}
            
            chart = self.tools.create_opex_chart(data)
            
            total_opex = data['amount_usd'].sum()
            text = f"**Operating Expenses Breakdown{' for ' + month if month else ''}:**\n\n"
            text += f"Total OpEx: ${total_opex:,.0f}\n\n"
            
            for _, row in data.iterrows():
                pct = (row['amount_usd'] / total_opex) * 100
                text += f"{row['category']}: ${row['amount_usd']:,.0f} ({pct:.1f}%)\n"
            
            return {"text": text, "chart": chart}
        
        # EBITDA
        elif 'ebitda' in question_lower:
            month = self.extract_month(question)
            ebitda_data = self.tools.get_ebitda(month)
            
            if "error" in ebitda_data:
                return {"text": ebitda_data["error"], "chart": None}
            
            text = f"**EBITDA Analysis{' for ' + month if month else ''}:**\n\n"
            text += f"Revenue: ${ebitda_data['revenue']:,.0f}\n"
            text += f"COGS: ${ebitda_data['cogs']:,.0f}\n"
            text += f"Opex: ${ebitda_data['opex']:,.0f}\n"
            text += f"EBITDA: ${ebitda_data['ebitda']:,.0f}"
            
            return {"text": text, "chart": None}

        # Cash Runway
        elif 'cash' in question_lower or 'runway' in question_lower or 'burn' in question_lower:
            runway_data = self.tools.calculate_cash_runway()
            
            if "error" in runway_data:
                return {"text": runway_data["error"], "chart": None}
            
            text = f"**Cash Runway Analysis:**\n\n"
            text += f"Current Cash: ${runway_data['current_cash']:,.0f}\n"
            text += f"Avg Monthly Burn: ${runway_data['avg_monthly_burn']:,.0f}\n"
            
            if runway_data['runway_months'] == float('inf'):
                text += f"Runway: Cash positive (no burn)"
            else:
                text += f"Runway: {runway_data['runway_months']:.1f} months"
            
            return {"text": text, "chart": None}

        # Gross Margin
        elif 'margin' in question_lower or 'gross' in question_lower:
            months = self.extract_months_count(question)
            data = self.tools.get_gross_margin_trend(months)
            
            if data.empty:
                return {"text": "No margin data found.", "chart": None}
            
            chart = self.tools.create_margin_chart(data)
            
            latest_margin = data['gross_margin_pct'].iloc[-1]
            avg_margin = data['gross_margin_pct'].mean()
            
            text = f"**Gross Margin Analysis:**\n\n"
            text += f"Latest Margin: {latest_margin:.1f}%\n"
            text += f"Average Margin: {avg_margin:.1f}%\n"
            
            if len(data) > 1:
                trend = "increasing" if data['gross_margin_pct'].iloc[-1] > data['gross_margin_pct'].iloc[0] else "decreasing"
                text += f"Trend: {trend.title()}"
            
            return {"text": text, "chart": chart}
        
        # Revenue vs Budget
        elif 'revenue' in question_lower or 'budget' in question_lower:
            month = self.extract_month(question)
            data = self.tools.get_revenue_vs_budget(month)
            
            if data.empty:
                return {"text": "No revenue data found for the specified period.", "chart": None}
            
            chart = self.tools.create_revenue_chart(data)
            
            if month:
                row = data.iloc[0]
                text = f"**Revenue vs Budget for {month}:**\n\n"
                text += f"Actual: ${row['amount_usd_actual']:,.0f}\n"
                text += f"Budget: ${row['amount_usd_budget']:,.0f}\n"
                text += f"Variance: ${row['variance']:,.0f} ({row['variance_pct']:.1f}%)"
            else:
                total_actual = data['amount_usd_actual'].sum()
                total_budget = data['amount_usd_budget'].sum()
                total_variance = total_actual - total_budget
                variance_pct = (total_variance / total_budget) * 100
                
                text = f"**Revenue vs Budget Summary:**\n\n"
                text += f"Total Actual: ${total_actual:,.0f}\n"
                text += f"Total Budget: ${total_budget:,.0f}\n"
                text += f"Total Variance: ${total_variance:,.0f} ({variance_pct:.1f}%)"
            
            return {"text": text, "chart": chart}
        
        else:
            return {
                "text": "I can help you with:\nRevenue vs budget analysis\nGross margin trends\nOperating expenses breakdown\nEBITDA calculation\nCash runway analysis\n\nTry asking:\n'What was February 2024 revenue vs budget?'\n'Show gross margin for last 3 months'\n'Break down Opex by category for February 2024'\n'What is our EBITDA?'\n'What is our cash runway?'",
                "chart": None
            }