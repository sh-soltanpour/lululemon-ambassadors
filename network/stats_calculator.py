import json
import networkx as nx
from networkx.algorithms.core import k_core
from networkx.algorithms.clique import find_cliques
from networkx.algorithms.assortativity import degree_assortativity_coefficient
from networkx.algorithms.components import number_connected_components, number_strongly_connected_components, \
    is_strongly_connected, is_connected
from networkx.algorithms.shortest_paths.generic import average_shortest_path_length
from networkx.algorithms.distance_measures import diameter
from networkx.algorithms.cluster import clustering, average_clustering
from networkx.algorithms.wiener import wiener_index

from network.builder import build_network, extract


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
