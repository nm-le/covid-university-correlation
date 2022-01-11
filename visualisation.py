"""
Takes classes using filter.py as data, outputs graphs.
"""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import filter

###############################################################################
# Part 1 - Visualizing impact scores
###############################################################################


def plot_covid():
    for uni in filter.uni_list:
        graph_individual_regional_covid(uni)


def plot_impacts():
    for uni in filter.uni_list:
        graph_uni_impact_score(uni)


def graph_uni_impact_score(uni: filter.University):
    """Graphs a universities' impact scores against """
    # x axis values
    x = np.array([x for x in uni.impact_dic.keys()])
    # y axis values
    y = np.array([x for x in uni.impact_dic.values()])
    plt.axes().set_xlim(0, 80)
    # plotting the points
    plt.plot(x, y, 'o', color='b', label='data')

    # naming the x-axis
    plt.xlabel('Weeks since March 20, 2020')

    # naming the y-axis
    plt.ylabel('Cumulative impact score')

    z = np.polyfit(x, y, 12)
    p = np.poly1d(z)

    plt.plot(x, p(x), "r-", label='trendline')

    # r-squared
    yhat = p(x)
    ybar = np.sum(y) / len(y)
    ssreg = np.sum((yhat - ybar) ** 2)
    sstot = np.sum((y - ybar) ** 2)
    r_sq = round((ssreg / sstot), 3)

    # title
    title = f'{uni.display_name} impact scores (r-squared = {str(r_sq)})'
    plt.title(title)

    # plot settings
    plt.xticks(range(min(x), max(x), 10))
    # function to save the plot
    plt.savefig(Path('output') / ('impact_' +
                uni.display_name + '.jpeg'), dpi=300)
    plt.clf()


def graph_individual_regional_covid(uni: filter.University):
    """Returns the graph of a singular CSV file, 
    plotting COVID-19 cases against day since March 20, 2020. """
    # x axis values
    x = np.array([x for x in uni.covid_dic.keys()])
    # y axis values
    y = np.array([y for y in uni.covid_dic.values()])
    plt.axes().set_xlim(0, 80)

    # plotting the points
    plt.plot(x, y, 'o', color='g', label='data')

    # naming the x-axis
    plt.xlabel('Weeks since March 20, 2020')

    # naming the y-axis
    plt.ylabel('COVID-cases')

    z = np.polyfit(x, y, 12)
    p = np.poly1d(z)

    plt.plot(x, p(x), "r-", label='trendline')

    # r-squared
    yhat = p(x)
    ybar = np.sum(y) / len(y)
    ssreg = np.sum((yhat - ybar) ** 2)
    sstot = np.sum((y - ybar) ** 2)
    r_sq = round((ssreg / sstot), 3)

    # title
    title = f'{uni.display_name} related COVID-cases (r-squared = {str(r_sq)})'
    plt.title(title)

    # plot settings
    plt.xticks(range(min(x), max(x), 10))

    # function to save plot
    plt.savefig(Path('output') / ('covid_' +
                uni.display_name + '.jpeg'), dpi=300)
    plt.clf()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'math'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
