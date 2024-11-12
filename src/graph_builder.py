# src/graph_operations.py
import networkx as nx
import matplotlib.pyplot as plt
from graphrag import GraphDatabase
from langgraph import SemanticGraph

def create_dynamic_graph(data):
    """Create a graph representation of data using networkx."""
    G = nx.DiGraph()
    for host, details in data.items():
        G.add_node(host, type='host')
        for port, service in details['ports']:
            G.add_node(port, type='port')
            G.add_edge(host, port)
            G.add_node(service, type='service')
            G.add_edge(port, service)
    return G

def visualize_graph(G):
    """Visualize the graph with matplotlib."""
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10)
    plt.title("Dynamic Graph Visualization")
    plt.show()

def check_vulnerabilities_inference(graph_db, query):
    """Query the graph database for vulnerabilities."""
    # Using raggraph for semantic retrieval of vulnerabilities
    results = graph_db.query(query)
    return results

def semantic_search(graph_db, semantic_graph, query):
    """Perform a semantic search using langgraph."""
    results = semantic_graph.search(query)
    return results