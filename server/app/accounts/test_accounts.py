from app.accounts import accounts_analysis


print(accounts_analysis.get_checkings_stats("4048842018"))
print(accounts_analysis.get_checkings_stats("4082013554"))
print(accounts_analysis.get_checkings_stats("2019535950"))
print(accounts_analysis.get_checkings_stats("7323109043"))

print(accounts_analysis.get_savings_stats("4048842018"))
print(accounts_analysis.get_savings_stats("4082013554"))
print(accounts_analysis.get_savings_stats("2019535950"))
print(accounts_analysis.get_savings_stats("7323109043"))

# accounts_analysis.display_accounts()