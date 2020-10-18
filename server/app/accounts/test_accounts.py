from app.accounts import accounts_analysis


for number in ["4048842018", "4082013554", "2019535950", "7323109043", '9393']:
    print("|||||||||||||||||||||||------------")
    print(accounts_analysis.get_username(number))
    print("- -")
    print("CATEGORY")
    print(accounts_analysis.get_category(number))
    print("- -")
    print(accounts_analysis.get_purchase_breakdown(number))
    print("- -")
    print(accounts_analysis.get_savings_breakdown(number))
    print("- -")

