import json
import streamlit as st
from streamlit_echarts import st_echarts

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def render_graph(data, width="100%", height="600px", label_font_size=12):
    option = {
        "tooltip": {},
        "legend": [
            {
                "data": [category["name"] for category in data["categories"]]
            }
        ],
        "series": [
            {
                "type": "graph",
                "layout": "force",
                "data": data["nodes"],
                "links": data["links"],
                "categories": data["categories"],
                "roam": True,
                "label": {
                    "show": True,
                    "position": "right",
                    "fontSize": label_font_size  # Adjust the font size here
                },
                "draggable": True,
                "force": {
                    "repulsion": 400
                },
            }
        ]
    }

    # Use st_echarts with events
    events = {
        "click": "function(params) { return params.data; }"
    }
    
    selected_node = st_echarts(options=option, width=width, height=height, events=events)
    
    return selected_node



def generate_generic_graph_data():
    nodes = []
    links = []

    central_node = {"name": "Central Node", "value": 10, "category": 0, "symbolSize": 50}
    nodes.append(central_node)

    subnode_counter = 1
    for i in range(1, 6):
        subnode = {"name": f"Subnode {i}", "value": 8, "category": i, "symbolSize": 40}
        nodes.append(subnode)
        links.append({"source": central_node["name"], "target": subnode["name"]})
        
        for _ in range(1, 6):
            sub_subnode = {"name": f"Node {subnode_counter}", "value": 6, "category": i, "symbolSize": 30}
            nodes.append(sub_subnode)
            links.append({"source": subnode["name"], "target": sub_subnode["name"]})
            subnode_counter += 1

    categories = [ {"name": f"{category}"} for category in range(6) ]
 

    data = {"nodes": nodes, "links": links, "categories": categories}
    return data


def render_generic_graph(data, width="100%", height="600px", label_font_size=12):
    option = {
        "tooltip": {},
        "legend": [
            {
                "data": [category["name"] for category in data["categories"]]
            }
        ],
        "series": [
            {
                "type": "graph",
                "layout": "force",
                "data": data["nodes"],
                "links": data["links"],
                "categories": data["categories"],
                "roam": True,
                "label": {
                    "show": True,
                    "position": "right",
                    "fontSize": label_font_size
                },
                "draggable": True,
                "force": {
                    "repulsion": 400
                },
            }
        ]
    }

    events = {
        "click": "function(params) { return params.data; }"
    }
    
    selected_node = st_echarts(options=option, width=width, height=height, events=events)
    
    return selected_node
