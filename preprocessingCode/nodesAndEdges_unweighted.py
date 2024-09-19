def count_nodes_edges(file_path):
    # Use a set to store unique edges and a set for nodes
    nodes = set()
    edges = set()

    # Open the file and read line by line
    with open(file_path, 'r') as file:
        for line in file:
            # Each line is in the format: node1 node2 weight
            parts = line.strip().split()
            if len(parts) == 2:  # Ensure it's a valid line with two nodes and a weight
                node1, node2 = int(parts[0]), int(parts[1])
                # Add the nodes to the set (nodes will automatically be unique)
                nodes.add(node1)
                nodes.add(node2)
                # Create a sorted tuple to represent an edge to avoid counting both (node1, node2) and (node2, node1)
                edge = tuple(sorted((node1, node2)))
                edges.add(edge)

    # The number of nodes is the size of the set
    node_count = len(nodes)
    # The number of edges is the size of the edges set
    edge_count = len(edges)

    return node_count, edge_count

file_path = 'undirect_graph.txt'
nodes, edges = count_nodes_edges(file_path)
print(f"Number of nodes: {nodes}")
print(f"Number of edges: {edges}")

