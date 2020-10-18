import io
from datetime import datetime
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
        date = datetime.strptime(x["date"], '%Y-%m-%d').date()
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


def chart_purchase_breakdown(breakdown: dict):
    sns.set_theme()
    otherSize = 40
    std = 4
    largeUser = breakdown["largePurchasePercent"]["score"]
    smallUser = breakdown["smallPurchasePercent"]["score"]
    largeAverage = np.random.normal(
        breakdown["largePurchasePercent"]["classAverage"], scale=std, size=otherSize)
    smallAverage = np.random.normal(
        breakdown["smallPurchasePercent"]["classAverage"], scale=std, size=otherSize)

    data = pd.DataFrame({"A": ["small", "large"], "B": [
                        smallUser, largeUser], "C": ["you", "you"]})

    for i in range(otherSize):
        frame = pd.DataFrame(
            [["large", largeAverage[i], "average"]], columns=list("ABC"))
        data = data.append(frame)
        frame = pd.DataFrame(
            [["small", smallAverage[i], "average"]], columns=list("ABC"))
        data = data.append(frame)

    f, ax = plt.subplots()
    sns.swarmplot(data=data, x="A", y="B", hue="C", palette="mako", size=8)
    ax.set_title("Purchase Breakdown",
                 fontname="geneva", fontsize=20)
    ax.set(xlabel='Type of Purchase', ylabel='Percentage of Purchases')
    format_ax(ax)
    plt.legend(title="")

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return img


def chart_portfolio_performance(pData: dict):
    def get_date(milli):
        return datetime.fromtimestamp(milli/1000).strftime("%b")
    sns.set_theme()
    palette = sns.color_palette("mako_r", 6)
    performance = np.array(pData["performanceData"])
    value = list(map(get_date, performance[:, 0]))
    change = performance[:, 1]

    data = pd.DataFrame({"Value": value, "Change": change})

    f, ax = plt.subplots()
    sns.lineplot(data=data, x="Value", y="Change", palette=palette)
    ax.set_title("Portfolio Performance",
                 fontname="geneva", fontsize=20)
    format_ax(ax)
    ax.set(xlabel='')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return img


def chart_stock_performance(pData: dict):
    def get_date(milli):
        return datetime.fromtimestamp(milli/1000).strftime("%b")
    sns.set_theme()
    palette = sns.color_palette("mako_r", 6)
    performance = np.array(pData["performanceData"])
    value = list(map(get_date, performance[:, 0]))
    change = performance[:, 1]

    data = pd.DataFrame({"Value": value, "Change": change})

    f, ax = plt.subplots()
    sns.lineplot(data=data, x="Value", y="Change", palette=palette)
    ax.set_title("Portfolio Performance",
                 fontname="geneva", fontsize=20)
    format_ax(ax)
    ax.set(xlabel='')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return img
