import re
import requests
import matplotlib.pyplot as plt
import networkx as nx
from sentence_transformers import SentenceTransformer, util

def parse_nmap_output(raw_output):
    hosts = {}
    host_pattern = r"Nmap scan report for (\S+)"
    port_pattern = r"(\d+)/tcp\s+open\s+(\S+)"
    
    current_host = None
    for line in raw_output.splitlines():
        host_match = re.search(host_pattern, line)
        if host_match:
            current_host = host_match.group(1)
            hosts[current_host] = {'ports': [], 'vulnerabilities': []}
        
        port_match = re.search(port_pattern, line)
        if port_match and current_host:
            port = port_match.group(1)
            service = port_match.group(2)
            hosts[current_host]['ports'].append((port, service))
    
    return hosts

def create_dynamic_graph(data):
    G = nx.DiGraph()

    for host, details in data.items():
        if not G.has_node(host):
            G.add_node(host, type='host')

        for port, service in details['ports']:
            if not G.has_node(port):
                G.add_node(port, type='port')
                G.add_edge(host, port)

            if not G.has_node(service):
                G.add_node(service, type='service')
                G.add_edge(port, service)

    return G

def visualize_graph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_color='black', font_weight='bold', edge_color='gray')
    plt.title("Dynamic Graph Visualization")
    plt.axis('off')
    plt.show()

def check_vulnerabilities_inference(graph, vulnerability_query):
    # Placeholder logic for checking vulnerabilities
    if "ABC" in vulnerability_query:
        return "No hosts are vulnerable to ABC."
    return "Vulnerability check completed."

def main():
    # Raw unstructured text outputs
    nmap_output = """
    Nmap scan report for 10.10.11.248
    PORT     STATE SERVICE REASON
    22/tcp   open  ssh     syn-ack
    80/tcp   open  http    syn-ack
    389/tcp  open  ldap    syn-ack
    443/tcp  open  https   syn-ack
    5667/tcp open  unknown syn-ack
    """
    
    # Step 1: Parse outputs
    nmap_data = parse_nmap_output(nmap_output)
    print("Parsed Nmap Data:", nmap_data)

    # Step 2: Create the dynamic graph
    graph = create_dynamic_graph(nmap_data)

    # Step 3: Visualize the graph
    visualize_graph(graph)

    # Step 4: Inference for vulnerabilities
    vulnerability_query = "Are there any hosts vulnerable to ABC?"
    response = check_vulnerabilities_inference(graph, vulnerability_query)
    print("LLM Response:", response)

if __name__ == "__main__":
    main()

from utils import fetch_data

def run_inference(url):
    data = fetch_data(url)
    if data:
        # Process the data for inference
        print("Running inference on data...")
        # Your inference logic here

if __name__ == "__main__":
    url = "https://www.freecodecamp.org/news/sense-walkthrough-hackthebox/"
    url = "https://medium.com/@heyrm/usage-machine-hackthebox-writeup-journey-through-exploitation-16397895490f"
    run_inference(url)    