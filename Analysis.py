import random
import networkx as nx
import matplotlib.pyplot as plt
from EoN import fast_SIR

# 2a,2b
# Load the network from file
G = nx.read_edgelist('Edges.csv', delimiter=',', nodetype=int, create_using=nx.DiGraph())

print("Number of nodes:", G.number_of_nodes())
print("Number of edges:", G.number_of_edges())

# Calculate the degree centrality for each node
degree_centrality = nx.degree_centrality(G)

print("Before between")
# Calculate the betweenness centrality for each node using k approximation
betweenness_centrality = nx.betweenness_centrality(G, k=400)
print("After between")

# Define the transmission rate
transmission_rate = 0.1

# Define the number of simulations to run
num_simulations = 10

# Define a list to store the Ti and Di values for each node
data_points, data_points1 = [], []

# Loop over the two centrality measures
for centrality_measure in [degree_centrality, betweenness_centrality]:

    # Loop over the 10 simulations with the most central node initially infected
    for i in range(num_simulations):
        infected_node = max(centrality_measure, key=centrality_measure.get)
        t, S, I, R = fast_SIR(G, transmission_rate, rho=None, gamma=0, tmin=0, tmax=50)

        for node_index, node in enumerate(G.nodes()):
            if node != infected_node:
                try:
                    distance = nx.shortest_path_length(G, infected_node, node)
                except nx.exception.NetworkXNoPath:
                    distance = float("inf")
                if node_index > len(I) - 1:
                    time_to_infect = float("inf")
                else:
                    time_to_infect = I[node_index]
                data_points.append((time_to_infect, distance))

    # Loop over the 10 simulations with the least central node initially infected
    for i in range(num_simulations):
        infected_node = min(centrality_measure, key=centrality_measure.get)
        t, S, I, R = fast_SIR(G, transmission_rate, rho=None, gamma=0, tmin=0, tmax=50)

        for node_index, node in enumerate(G.nodes()):
            if node != infected_node:
                try:
                    distance = nx.shortest_path_length(G, infected_node, node)
                except nx.exception.NetworkXNoPath:
                    distance = float("inf")
                if node_index > len(I) - 1:
                    time_to_infect = float("inf")
                else:
                    time_to_infect = I[node_index]
                data_points1.append((time_to_infect, distance))

# Plot the Ti vs Di data points
x = [p[1] for p in data_points]
y = [p[0] for p in data_points]
z = [p[1] for p in data_points1]
w = [p[0] for p in data_points1]

plt.scatter(x, y, label="Max central infected")
plt.scatter(z, w, label="Min central infected")
plt.legend()
plt.xlabel('Di (Distance From Initially Infected)')
plt.ylabel('Ti (Time Steps till infection)')
plt.title("mix/max central")
plt.show()


# # 3a, 3b
first_community = nx.read_edgelist('1st_mod_class_4_subgraph.csv', delimiter=',', nodetype=int,
                                   create_using=nx.DiGraph())
second_community = nx.read_edgelist('2nd_mod_class_2_subgraph.csv', delimiter=',', nodetype=int,
                                    create_using=nx.DiGraph())
third_community = nx.read_edgelist('3rd_mod_class_15_subgraph.csv', delimiter=',', nodetype=int,
                                   create_using=nx.DiGraph())
fourth_community = nx.read_edgelist('4th_mod_class_10_subgraph.csv', delimiter=',', nodetype=int,
                                    create_using=nx.DiGraph())
fifth_community = nx.read_edgelist('5th_mod_class_11_subgraph.csv', delimiter=',', nodetype=int,
                                   create_using=nx.DiGraph())

transmission_rate = 0.1
for i, community in enumerate([first_community, second_community, third_community, fourth_community, fifth_community]):
    print("Number of nodes:", community.number_of_nodes())
    print("Number of edges:", community.number_of_edges(), "\n")
    start_node = random.choice(list(community.nodes))

    t, S, I, R = fast_SIR(community, transmission_rate, initial_infecteds=[start_node], gamma=0)

    degree_centrality = nx.degree_centrality(community)
    avg_degree_centrality = sum(degree_centrality.values()) / len(degree_centrality)
    print(avg_degree_centrality)

    # random graphs
    random_graph = nx.gnm_random_graph(n=community.number_of_nodes(), m=community.number_of_edges())
    start_node_random = random.choice(list(random_graph.nodes))
    t1, S, I1, R = fast_SIR(random_graph, transmission_rate, initial_infecteds=[start_node_random], gamma=0)

    degree_centrality = nx.degree_centrality(random_graph)
    avg_degree_centrality = sum(degree_centrality.values()) / len(degree_centrality)
    print(avg_degree_centrality)

    plt.scatter(t, I, label='Community Data')
    plt.scatter(t1, I1, label='Random Graph Data')
    plt.legend()
    plt.xlabel('t')
    plt.ylabel(f'N{i + 1}')
    plt.title(f"Rank {i + 1} community")
    plt.show()
