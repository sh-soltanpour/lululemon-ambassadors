import os
import time
from datetime import datetime
from typing import List, Tuple, Dict
import json
import random
import networkx as nx
from networkx.algorithms.core import k_core
from networkx.algorithms.clique import find_cliques
from networkx.algorithms.assortativity import degree_assortativity_coefficient
from networkx.algorithms.components import number_connected_components, number_strongly_connected_components, \
    is_strongly_connected, is_connected
from networkx.algorithms.cluster import clustering, average_clustering
from networkx.algorithms.wiener import wiener_index

import networkx as nx

from networkx.algorithms.shortest_paths.generic import average_shortest_path_length
from networkx.algorithms.distance_measures import diameter

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('tkagg')
AMBASSADORS_LIST = 'list.json'


def extract(path: str) -> Dict[str, List[Dict]]:
    area_list = os.listdir(path)
    areas = {}
    for area in area_list:
        ambassadors = json.load(open(f"{path}/{area}"))
        for ambassador in ambassadors:
            followers_usernames = list(map(lambda x: x['username'], ambassador.get('followers', [])))
            ambassador['followers'] = followers_usernames
        areas[area] = ambassadors
    return areas


def build_network(ambassadors: List[Dict]) -> nx.DiGraph:
    g = nx.DiGraph()
    colors = {}
    main_handles = []
    for ambassador in ambassadors:
        city = ambassador['city']
        handle = ambassador['instagram']
        if handle is None:
            continue
        colors[city] = {
            'r': random.randint(0, 255),
            'g': random.randint(0, 255),
            'b': random.randint(0, 255)
        }
        g.add_node(handle, viz={'color': {**colors[city], 'a': 1.0}}, bipartite=1)
        main_handles.append(handle)
    # print(colors)
    for ambassador in ambassadors:
        city = ambassador['city']
        for adj in ambassador.get('followers', []):
            if not g.has_node(adj):
                g.add_node(adj, viz={'color': {**colors[city], 'a': 1.0}}, bipartite=2, city=city)
    for ambassador in ambassadors:
        handle = ambassador['instagram']
        city = ambassador['city']
        for adj in ambassador.get('followers', []):
            if adj in main_handles:
                g.add_edge(adj, handle, viz={'color': {**colors[city], 'a': 1.0}})
            else:
                g.add_edge(adj, handle, viz={'color': {**colors[city], 'a': 1.0}})
    return g


def degree_distribution_log(g: nx.DiGraph):
    degrees = [g.degree(node) for node in g]
    kmin = 1
    kmax = max(degrees)
    # Get 10 logarithmically spaced bins between kmin and kmax
    bin_edges = np.logspace(np.log10(kmin), np.log10(kmax), num=10)
    # histogram the data into these bins
    density, _ = np.histogram(degrees, bins=bin_edges, density=True)
    fig = plt.figure(figsize=(6, 4))
    # "x" should be midpoint (IN LOG SPACE) of each bin
    log_be = np.log10(bin_edges)
    x = 10 ** ((log_be[1:] + log_be[:-1]) / 2)
    plt.loglog(x, density, marker='o', linestyle='none')
    plt.xlabel(r"degree $k$", fontsize=16)
    plt.ylabel(r"$P(k)$", fontsize=16)
    # remove right and top boundaries because they're ugly
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    # Show the plot
    plt.show()


def degree_distribution(g: nx.DiGraph):
    degrees = [g.degree(node) for node in g]
    kmin = 1
    kmax = max(degrees)
    # Get 20 logarithmically spaced bins between kmin and kmax
    bin_edges = np.linspace(kmin, kmax, num=10)
    # histogram the data into these bins
    density, _ = np.histogram(degrees, bins=bin_edges, density=True)
    fig = plt.figure(figsize=(6, 4))
    # "x" should be midpoint (IN LOG SPACE) of each bin
    log_be = np.log10(bin_edges)
    x = 10 ** ((log_be[1:] + log_be[:-1]) / 2)
    plt.plot(x, density, marker='o', linestyle='none')
    plt.xlabel(r"degree $k$", fontsize=16)
    plt.ylabel(r"$P(k)$", fontsize=16)
    # remove right and top boundaries because they're ugly
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    # Show the plot
    plt.show()


def count_cliques(areas_lists):
    for area in areas_lists:
        print(f"Area: {area}")
        graph = build_network(areas[f'{area}_ambassadors.json'])

        print("Getting k_Core")
        k_core_graph = k_core(graph, k=2)

        print("K core undirected")
        k_core_undirected = nx.DiGraph.to_undirected(k_core_graph)

        print("Enumerate all cliques")
        cliques = list(find_cliques(k_core_undirected))
        print(len(cliques))
        print([len(cliques[i]) for i in range(10)])

        print("----------------")

def find_wiener_index(areas_lists):
    for area in areas_lists:
        print(f"Area: {area}")
        graph = build_network(areas[f'{area}_ambassadors.json'])

        print("Getting k_Core")
        k_core_graph = k_core(graph, k=2)

        print("K core undirected")
        k_core_undirected = nx.DiGraph.to_undirected(k_core_graph)

        print("Wiener Index")
        print(wiener_index(k_core_undirected))
        print("----------------")

def assortativity(areas_lists):
    for area in areas_lists:
        print(f"Area: {area}")
        graph = build_network(areas[f'{area}_ambassadors.json'])

        print("Getting k_Core")
        k_core_graph = k_core(graph, k=2)

        print("Enumerate degree assortativity coefficient")
        print(degree_assortativity_coefficient(k_core_graph))
        print("----------------")



areas_lists = ['asia_1', 'asia_2', 'australia', 'europe', 'korea', 'uk', 'global', 'canada']
areas = extract('./ambassadors_lists')


def get_statistics(graph: nx.DiGraph):
    graph = nx.DiGraph.to_undirected(graph)
    graph = nx.k_core(graph, k=2)
    connected = nx.is_connected(graph)
    stat = {}
    stat['nodes'] = graph.number_of_nodes()
    stat['edges'] = graph.number_of_edges()
    stat['degrees'] = [d[1] for d in graph.degree()]
    stat['cc'] = nx.number_connected_components(graph)
    stat['average_clustering'] = average_clustering(graph)
    stat['average_shortest_path'] = average_shortest_path_length(graph)
    if connected:
        stat['diameter'] = diameter(graph)
    return stat


def create_null_models(areas_lists):
    RANDOM_GENERATION_NUM = 10
    for area in areas_lists:
        network_name = f'{area}_ambassadors.json'
        statistics_list = []
        graph = build_network(areas[network_name])
        graph = nx.DiGraph.to_undirected(graph)
        graph = nx.k_core(graph, k=2)
        nodes = graph.number_of_nodes()
        edges = graph.number_of_edges()
        degrees = [d[1] for d in graph.degree()]
        avg_degree = int(sum(degrees) / len(degrees))
        for i in range(RANDOM_GENERATION_NUM):
            rg = nx.barabasi_albert_graph(nodes, avg_degree)
            print("STATS")
            stats = get_statistics(rg)
            statistics_list.append(stats)
        with open(f"{network_name}_stats_random.json", 'w') as f:
            json.dump(statistics_list, f)
        print(f"{area} FIN")


create_null_models(areas_lists)
