import xml.etree.ElementTree as ET
import os
import re
from graphviz import Digraph

class XML_parser:
    def __init__(self, file_name):
        self.tree = ET.parse(file_name)

    def change_value(self, key, new_value):
        for name in self.tree.findall(".//" + key):
            name.text = new_value
        ET.dump(self.tree)
        
    def add_value(self, key, value):
        self.tree.getroot().set(key, value)
        ET.dump(self.tree)

    def get_value(self, key):
        finded_tags = self.tree.findall(".//"+key)
        if len(finded_tags) > 0:
            return finded_tags[0].text
        return None

class Graphviz_manager:

    def __init__(self):
        pass

    def create_graph(self, graph_name : str, dependecies):
        dot = Digraph(comment=graph_name)
        nodes = []

        def node_text(node):
            return node[0] + ' : ' + node[1]
        
        def node_key(node):
            return node[0]+'_'+node[1]

        for item in dependecies:
            node_from = item[0]
            node_to = item[1]
            node_from_key = node_key(node_from)
            node_to_key = node_key(node_to)

            if not node_from in nodes:
                dot.node(node_from_key, node_text(node_from))
                nodes.append(node_from)
            if not node_to in nodes:
                dot.node(node_to_key, node_text(node_to))
                nodes.append(node_to)
            dot.edge(node_from_key, node_to_key)
        dot.render('test-output/'+graph_name+'.gv', view=True)  # Сохранит и откроет PDF



keys = ["package_name", "url", "mode_test_dir", "file_name_graph", "mode_output"]
file = "temp.xml"
value = "value"
# tree = ET.parse(file)
# for key in keys:
#     print(f"{key} : {get_value(tree, key)}")

graphviz = Graphviz_manager()

test_depencies = [(('c', '0.7.0'), ('base', '1.2.0')), (('c', '0.7.0'), ('a', '0.2.0')), (('a', '0.2.0'), ('base', '1.0.0'))]
graphviz.create_graph("Graph", test_depencies)

