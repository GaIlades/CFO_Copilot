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
    
    def answer_question(self, question):
        """Answer revenue vs budget questions"""
        question_lower = question.lower()
        
        # Check if it's a revenue question
        if 'revenue' in question_lower or 'budget' in question_lower:
            month = self.extract_month(question)
            data = self.tools.get_revenue_vs_budget(month)
            
            if data.empty:
                return {"text": "No revenue data found for the specified period.", "chart": None}
            
            chart = self.tools.create_revenue_chart(data)
            
            # Format response
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
                "text": "I can help you with revenue vs budget analysis. Try asking:\n• 'What was February 2024 revenue vs budget?'\n• 'Show revenue vs budget'",
                "chart": None
            }