import io
import datetime
import seaborn as sns
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
matplotlib.use('Agg')


def format_ax(ax):

    for tick in ax.get_xticklabels():
        tick.set_fontname("geneva")
    for tick in ax.get_yticklabels():
        tick.set_fontname("geneva")


def chart_checking_account(user: dict):
    sns.set_theme(style="whitegrid", palette="muted")
    transactions = user["transactions"]

    collected_transactions = {}

    for x in transactions:
        date = datetime.datetime.strptime(x["date"], '%Y-%m-%d').date()
        amount = x["amount"]
        if date in collected_transactions:
            collected_transactions[date] += amount
        else:
            collected_transactions[date] = amount

    sorted_transactions = sorted(
        list(collected_transactions.items()), key=lambda x: x[0])

    sum_transactions = []
    sum = 0
    for date, transaction in sorted_transactions:

        sum += transaction
        sum_transactions.append(sum)

    dates = np.array(list(map(lambda x: x[0], sorted_transactions)))
    daily_transactions = np.array(
        list(map(lambda x: x[1], sorted_transactions)))
    sum_transactions = np.array(sum_transactions)

    data = pd.DataFrame(
        {"dates": dates, "daily_transactions": daily_transactions, "sum_transactions": sum_transactions})
    data = pd.melt(data, id_vars="dates", var_name="type", value_name="amount")

    f, ax = plt.subplots()
    sns.barplot(x="dates", y="amount", data=data, hue='type', palette="rocket")
    # sns.histplot(data=data, x="dates", hue="type", multiple="layer")
    format_ax(ax)
    ax.set_title("Checking Account Transactions",
                 fontname="geneva", fontsize=20)
    ax.grid(axis='x')
    ax.xaxis.set_major_locator(ticker.LinearLocator(6))
    sns.despine(f, left=True, bottom=True)
    plt.legend()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return img
