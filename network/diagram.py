import json
import matplotlib.pyplot as plt
import numpy as np
import powerlaw
from networkx import k_core

from builder import extract, build_network

areas_lists = ['asia_1', 'asia_2', 'australia', 'europe', 'korea', 'uk', 'global', 'canada']


def average_factor(area):
    """ prints some general stats for graph of each area,
    including average of diameter, degree, average shortest path """
    with open(f"./null_model/{area}_ambassadors_stats_random.json") as f:
        data = json.load(f)
        list_of_factor = []
        for random_graph in data:
            list_of_factor.append(random_graph['diameter'])
        print(area)
        print(np.average(list_of_factor))
        print(np.std(list_of_factor))
        print("-----------------------")


def power_law_fit(degrees_list, area, draw_power_law_fit=True):
    """ Draws degree distribution for given graphs, also can print the power law fit on the diagram """
    for degseq in degrees_list:
        kmin = min(degseq)
        kmax = max(degseq)
        fit = powerlaw.Fit(degseq, xmin=1)

        # "x" should be midpoint (IN LOG SPACE) of each bin
        bin_edges = np.logspace(np.log10(kmin), np.log10(kmax), num=10)
        log_be = np.log10(bin_edges)
        x = 10 ** ((log_be[1:] + log_be[:-1]) / 2)
        x1 = np.logspace(0, np.log10(kmax))  # the max is the log(Max_Degree)
        y1 = x1 ** (-fit.power_law.alpha)  # Alpha value From above cell
        if draw_power_law_fit:
            plt.plot(x1, y1)
        density, _ = np.histogram(degseq, bins=bin_edges, density=True)
        plt.loglog(x, density, marker='o', linestyle='none')
        plt.xlabel(r"degree $k$", fontsize=16)
        plt.ylabel(r"$P(k)$", fontsize=16)
        # remove right and top boundaries because they're ugly
        ax = plt.gca()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')

    plt.savefig(f"./images/{area}-fit-randoms-log.png")


def create_plots_for_random_graphs():
    """
        Draws degree distribution with power law for null model graphs
        You should call this in your main function
    """
    for area in areas_lists:
        with open(f"./null_model/{area}_ambassadors_stats_random.json") as f:
            data = json.load(f)
        degrees_list = []
        for random_graph in data:
            degrees = random_graph['degrees']
            degrees_list.append(degrees)
        power_law_fit(degrees_list, area)


def create_plots_for_regions_with_fit():
    """
        Draws degree distribution with power law for original graphs
        You should call this in your main function
    """
    areas = extract('./ambassadors_lists')
    for area in areas_lists:
        graph = build_network(areas[f'{area}_ambassadors.json'])
        k_core_graph = k_core(graph, k=2)
        power_law_fit(k_core_graph, area, draw_power_law_fit=False)
