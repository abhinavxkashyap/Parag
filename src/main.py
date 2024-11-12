import re
import matplotlib.pyplot as plt
import networkx as nx

def parse_nmap_output(raw_output):
    hosts = {}
    # Regex to find the host and its open ports
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

def parse_ffuf_output(raw_output):
    # Regex to find the URLs and their statuses
    url_pattern = r"(\S+)\s+\[Status:\s+(\d+)"
    urls = []
    
    for line in raw_output.splitlines():
        url_match = re.search(url_pattern, line)
        if url_match:
            urls.append((url_match.group(1), url_match.group(2)))
    
    return urls

def create_dynamic_graph(data):
    G = nx.DiGraph()

    for host, details in data.items():
        # Add host node
        if not G.has_node(host):
            G.add_node(host, type='host')

        for port, service in details['ports']:
            # Add port node and edge to host
            if not G.has_node(port):
                G.add_node(port, type='port')
                G.add_edge(host, port)

            # Add service node and edge to port
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

def check_vulnerabilities(graph, service):
    # Check if there are any vulnerabilities associated with the service
    if graph.has_node(service):
        # Here you would typically query an LLM or a database for vulnerabilities
        return f"Vulnerabilities found for service: {service}"
    return f"No vulnerabilities found for service: {service}"

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
    
    ffuf_output = """
    images                  [Status: 301]
    index.php               [Status: 302]
    login.php               [Status: 200]
    help                    [Status: 301]
    """
    
    # Parse outputs
    nmap_data = parse_nmap_output(nmap_output)
    ffuf_data = parse_ffuf_output(ffuf_output)

    # Create the dynamic graph
    graph = create_dynamic_graph(nmap_data)

    # Visualize the graph
    visualize_graph(graph)

    # Check for vulnerabilities
    for service in ['ssh', 'http', 'ldap', 'https']:
        print(check_vulnerabilities(graph, service))

if __name__ == "__main__":
    main()

from graph_builder import build_graph
from inference_pipeline import run_inference

def main():
    url = "https://www.freecodecamp.org/news/sense-walkthrough-hackthebox/"
    build_graph(url)
    run_inference(url)

if __name__ == "__main__":
    main()    

import logging
from graph_builder import build_graph
from inference_pipeline import run_inference

# Configure logging
logging.basicConfig(level=logging.INFO)

def main():
    url = "https://www.freecodecamp.org/news/sense-walkthrough-hackthebox/"
    url = "https://medium.com/@heyrm/usage-machine-hackthebox-writeup-journey-through-exploitation-16397895490f"
    logging.info("Starting the main process.")
    
    logging.info("Building graph...")
    build_graph(url)
    
    logging.info("Running inference...")
    run_inference(url)
    
    logging.info("Process completed.")

if __name__ == "__main__":
    main()    