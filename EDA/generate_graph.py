import pandas as pd
from io import StringIO
import json

# files & main categories
data = {"Automotive Manufacture" : "sectors_nodes/fabricacion_automotores.csv",
        "Energy and Water": "sectors_nodes/energia_agua.csv",
        "Fashion": "sectors_nodes/moda.csv",
        "Turism": "sectors_nodes/turismo.csv",
        "Health": "sectors_nodes/salud.csv"}


# Read the CSV data into a DataFrame
for key, value in data.items():

    print(f"Reading file {value}")

    main_category_name = key
    df = pd.read_csv(value)
    
    # Prepare nodes, links, and categories for the JSON structure
    nodes = []
    links = []
    categories = []
    node_names = set()

    for _, row in df.iterrows():
        parent, child = row['Nodo'], row['Subnodo']
        if pd.notna(parent):
            if parent not in node_names:
                nodes.append({"name": parent, "category": len(categories)+1, "symbolSize": 30})
                categories.append({"name": parent})
                node_names.add(parent)
            parent_category = parent

        if pd.notna(child):
            if child not in node_names:
                nodes.append({"name": child, "category": categories.index({"name": parent_category})+1, "symbolSize": 20})
                node_names.add(child)
            links.append({"source": parent_category, "target": child})


    if main_category_name not in node_names:
        nodes.insert(0, {"name": main_category_name, "category": 0, "symbolSize": 50})
        categories.insert(0, {"name": main_category_name})
        node_names.add(main_category_name)

    for category in categories[1:]:
        links.append({"source": main_category_name, "target": category["name"]})

    graph_data = {
        "nodes": nodes,
        "links": links,
        "categories": categories
    }

    # Convert to JSON string (for printing or saving to a file)
    graph_json = json.dumps(graph_data, indent=2)
    #print(graph_json)

    json_name = key.lower().replace(" ", "_")

    with open(f"graphs/{json_name}.json", "w") as outfile:
        outfile.write(graph_json)

    print(f"Saving file {json_name}.json")