import json
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
from IPython.display import display
from networkx.drawing.interactive import (
    VertexText,
    annotation,
    EdgeTextRotation,
    draw_networkx_edge_labels,
    draw_networkx_edges,
    draw_networkx_nodes,
    draw_networkx_labels,
    InteractiveGraph,
)

def load_json_data(filepath):
    """Load JSON data from a file."""
    with open(filepath, 'r') as file:
        json_text = file.read()
        json_text = json_text.strip('`\r\n ').removeprefix('json')
        return json.loads(json_text)

def build_graph(node, graph, parent=None, depth=0):
    """Recursively add nodes and edges to the graph based on the JSON data, adjusting node size by depth."""
    node_label = f"{node['user']}: {node['text']}\nAwk: {node['awkwardnessLevel']}, Goal: {node['goalAchievementLikelihood']}"
    graph.add_node(node['nodeNumber'], label=node_label, size=3000 / (1 + depth), layer=depth)
    if parent is not None:
        graph.add_edge(parent, node['nodeNumber'])
    for child in node.get('children', []):
        build_graph(child, graph, node['nodeNumber'], depth + 1)

# def draw_graph(graph):
#     """Draw the graph using matplotlib with a vertical layout and diamond-shaped nodes, enhancing label visibility."""
#     pos = nx.multipartite_layout(graph, subset_key="layer")  # Vertical layout
#     sizes = [graph.nodes[node]['size'] for node in graph.nodes()]
#     layers = [graph.nodes[node]['layer'] for node in graph.nodes()]
#     max_layer = max(layers) if layers else 1  # Prevent division by zero

#     # Create color gradient based on the layer
#     colors = [plt.cm.plasma(layer / max_layer) for layer in layers]  # Purple gradient

#     plt.figure(figsize=(60, 40))
#     plt.style.use('dark_background')  # Dark background style

#     # Draw nodes with diamond shape
#     nx.draw(graph, pos, node_size=sizes, node_color=colors, with_labels=False, font_color='white', edge_color='gray', alpha=0.7, node_shape='d')

#     # Drawing labels with improved visibility
#     for node in graph.nodes():
#         node_pos = pos[node]
#         plt.text(node_pos[0], node_pos[1], graph.nodes[node]['label'], fontsize=9, fontweight='bold',
#                  ha='center', va='center_baseline', color='white', bbox=dict(facecolor='black', alpha=0.5, edgecolor='none'))

#     plt.title('Decision Tree Visualization', color='white')
#     plt.show()
def draw_graph(graph):
    """Draw the interactive graph using networkx and IPython with circular nodes, edge weights, edge labels, and custom layouts."""
    pos = graphviz_layout(graph, prog='dot', args='-Glabeljust="left" -Gfontsize=32')  # Circular layout

    # Create and display the interactive graph object
    interactive_graph = InteractiveGraph(pos, graph)
    display(interactive_graph)

    # Add custom annotations
    annotation(graph,
                pos=pos,
                text="Awkwardness Level (lower is better)",
                loc='top',
                fontsize=12,
                )

    annotation(graph,
                pos=pos,
                text="Goal Achievement Likelihood",
                loc='bottom',
                fontsize=12,
                )

    # Custom drawing functions for nodes, edges, and labels
    def draw_custom_nodes(graph, pos):
        draw_networkx_nodes(graph, pos, nodelist=graph.nodes(), node_size=2000, node_shape='o',
                            node_color='#ffffff', alpha=0.8, node_zorder=2, linewidths=0.8)

    def draw_custom_edges(graph, pos):
        draw_networkx_edges(graph, pos, edgelist=graph.edges(), alpha=0.4, width=1, edge_color='#9d9d9d')
        draw_networkx_edge_labels(graph, pos, label_pos=0.5, font_size=8, edge_labels=nx.get_edge_attributes(graph, 'weight'), rotate=False,
                                  horizontalalignment='center', verticalalignment='center', font_color='#000000', bbox=dict(facecolor='#ffffff', edgecolor='none', alpha=0.5))

    def draw_custom_labels(graph, pos):
        draw_networkx_labels(graph, pos, font_family='calibri', font_size=10, font_weight='normal', font_color='#000000',
                             horizontalalignment='center', verticalalignment='center')

    # Attach custom drawing functions to the interactive graph
    draw_custom_nodes(graph, pos)
    draw_custom_edges(graph, pos)
    draw_custom_labels(graph, pos)

    # Add additional features for user interaction
    interactive_graph.add_features([VertexText("Node Information"), EdgeTextRotation()])
    interactive_graph.set_edge_style_params(rot_dist=10, rot_align='center')

    plt.show()
def main():
    data = load_json_data('analysis_results.txt')
    G = nx.DiGraph()
    build_graph(data, G)
    draw_graph(G)

if __name__ == '__main__':
    main()