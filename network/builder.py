import os
from typing import List, Tuple, Dict
import json
import random
import networkx as nx
from networkx.algorithms import smallworld
from networkx.algorithms.core import k_core
from networkx.algorithms import richclub
from networkx.algorithms.clique import find_cliques
from networkx.algorithms.assortativity import degree_assortativity_coefficient
from networkx.algorithms.wiener import wiener_index
from networkx.algorithms.components import is_connected
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use( 'tkagg' )
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
    fig = plt.figure(figsize=(6,4))
    # "x" should be midpoint (IN LOG SPACE) of each bin
    log_be = np.log10(bin_edges)
    x = 10**((log_be[1:] + log_be[:-1])/2)
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
    fig = plt.figure(figsize=(6,4))
    # "x" should be midpoint (IN LOG SPACE) of each bin
    log_be = np.log10(bin_edges)
    x = 10**((log_be[1:] + log_be[:-1])/2)
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

def assortativity(areas_lists):
    for area in areas_lists:
        print(f"Area: {area}")
        graph = build_network(areas[f'{area}_ambassadors.json'])

        print("Getting k_Core")
        k_core_graph = k_core(graph, k=2)

        print("Enumerate degree assortativity coefficient")
        print(degree_assortativity_coefficient(k_core_graph))
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

areas_lists = ['asia_1', 'asia_2', 'australia', 'canada', 'europe', 'global', 'korea', 'uk']
areas = extract('./ambassadors_lists')
find_wiener_index(areas_lists)
