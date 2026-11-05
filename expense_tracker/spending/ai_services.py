from click import prompt
from google import genai


api_key="AQ.Ab8RN6Ko0KGwUjjiyBLeqqoNApLaT040ThmOwO3B2qO4UPhsBw"

client=genai.Client(api_key=api_key)

def budget_plan(response_data):
    # to calculate a budget plan using ai

    # extracting  monthly_total and category_total list wise
    monthly_total=response_data.get('monthly_total')
    category_total=response_data.get('category_total')

    # converting list into text for easy to understand by Ai
    category_summary=""

    for i in category_total:
        category_summary += f".{i.get('category')}-{i.get('total')}\n"

    prompt=f"""
    Act as an expert financial advisor specializing in family budgeting and pers

    Here is my monthly financial summary for last month:
    - Total Monthly Expense: ₹{monthly_total}
    - Category Breakdown: {category_summary}


    Based on this data, please provide a practical 1-month  budget plan:
    1. *Expense Analysis: Point out high-spending areas relative to typical Kerala cost of living.
    2. Optimized 1-Month Allocation Plan: Suggest a revised budget breakdown.
    3. Actionable Kerala-Specific Savings Tips:* Provide 3-4 realistic ways to cut costs in Kerala.
    """

    response=client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )
    print(response.text)
    return response.text