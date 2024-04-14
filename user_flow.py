import json
from pyvis.network import Network
import os 

def load_json_data(filepath):
    """Load JSON data from a file."""
    with open(filepath, 'r') as file:
        json_text = file.read()
        json_text = json_text.strip('`\r\n ').removeprefix('json')
        return json.loads(json_text)

def build_network(node, net, parent=None, depth=0):
    """Recursively add nodes and edges to the Pyvis network."""
    node_label = f"{node['user']}: {node['text']}\nAwk: {node['awkwardnessLevel']}, Goal: {node['goalAchievementLikelihood']}"
    net.add_node(node['nodeNumber'], label=node_label, title=node_label,
                 size=30 / (1 + depth), color=get_color(node['awkwardnessLevel']), depth=depth)
    if parent is not None:
        net.add_edge(parent, node['nodeNumber'])
    for child in node.get('children', []):
        build_network(child, net, node['nodeNumber'], depth + 1)
def get_color(awkwardness_level):
    """Map awkwardness level to color."""
    if awkwardness_level == "Low":
        return "green"
    elif awkwardness_level == "Medium":
        return "orange"
    elif awkwardness_level == "High":
        return "red"
    else:
        return "gray"
def main():
    data = load_json_data('analysis_results.txt')
    net = Network(notebook=True, height='600px', width='100%', bgcolor='#222222', font_color='white')
    net.barnes_hut()
    build_network(data, net)
    net.set_options("""
    var options = {
      "nodes": {
        "borderWidth": 4,
        "borderWidthSelected": 6
      },
      "edges": {
        "color": {
          "inherit": true
        },
        "smooth": false
      },
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -8000,
          "springLength": 200
        }
      }
    }
    """)

    net.show('decision_tree.html')

    file_path = "decision_tree.html"
    if os.path.exists(file_path):
        print(f"HTML file created successfully at: {os.path.abspath(file_path)}")
    else:
        print("Error: HTML file creation failed.")

if __name__ == '__main__':
    main()
