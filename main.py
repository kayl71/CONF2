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
import os
import re

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



class Package_parser:
    def __init__(self, dir_packages_path):
        self.dir_packages = {}
        self.dir_packages_dependecies = {}
        all_items_in_dir = os.listdir(dir_packages_path)
        files_only = list([item for item in all_items_in_dir if os.path.isfile(dir_packages_path + "/" + item)])

        for package_file in files_only:
            with open(dir_packages_path+'/'+package_file, 'r') as file:
                text = file.read()
                block_package = self.__get_block_dict__(text, "package")
                block_dependencies = self.__get_block_dict__(text, "dependencies")

                try:
                    package_name = block_package['name']
                    package_version = block_package['version']
                except Exception as e:
                    continue
                self.dir_packages[(package_name, package_version)] = package_file
                self.dir_packages_dependecies[(package_name, package_version)] = block_dependencies

    def __get_block_dict__(self, text, block_name):
        block_names = ["package", 'dependencies']
        block_dict = {}
        if not block_name in block_names:
            return None
        block_name = '[' + block_name + ']'
        text_without = text[text.find(block_name)+len(block_name)+1:]
        text_without = text_without[:text_without.find('[')]
        info = text_without.split('\n')
        for val in info:
            del_pos = val.find('=')
            if del_pos <= 0:
                continue
            key = val[:del_pos-1]
            value = val[del_pos+2:]
            value = re.sub('[ \'\"]', '', value)

            block_dict[key] = value
        return block_dict
    
    def _package_contain_(self, package_name, version = None):
        for key in self.dir_packages.keys():
            if version == None and key[0] == package_name:
                return True
            elif key[0] == package_name and key[1] == version:
                return True
        return False
    
    def _get_package_last_version_(self, package_name):
        last_version = '0.0.0'
        file_name = ""
        for key in self.dir_packages.keys():
            name = key[0]
            version = key[1]

            if name == package_name and version > last_version:
                last_version = version
                file_name = name
        if file_name == "":
            return None
        return self.dir_packages[(file_name, version)]


    def get_package_info(self, package_name, version = None):
        file_name = ""
        if version == None:
            file_name = self._get_package_last_version_(package_name)
        else:
            file_name = self.dir_packages[(package_name, version)]

        with open(self.dir_packages + '/' + file_name) as file:
            text = file.read()
            return self.__get_block_dict__(text, "package")
        
         
    def get_package_dependencies(self, package_name, version = None):
        file_name = ""
        if version == None:
            file_name = self._get_package_last_version_(package_name)
        else:
            file_name = self.dir_packages[(package_name, version)]

        with open(self.dir_packages + '/' + file_name) as file:
            text = file.read()
            return self.__get_block_dict__(text, "dependencies")
    
    def get_package_by_filename(self, filename : str):
        for item in self.dir_packages.items():
            if item[1] == filename:
                return item[0]
        return None

class Graph_manager:
    def __init__(self, package_parser : Package_parser):
        self.packages_depencies = package_parser.dir_packages_dependecies
        self.depencies = []
        for key in self.packages_depencies:
            for key_key in self.packages_depencies[key]:
                self.depencies.append( (key, (key_key, self.packages_depencies[key][key_key])) )


    def get_array_dependecies_from_package_to_level(self, package_name : str, package_version : str, level = 1):
        queue = []
        visited = []
        depencies = []
        queue.append(((package_name, package_version), level))
        visited.append((package_name, package_version))

        while len(queue) > 0:
            cur_package, cur_level = queue.pop(0)
            if cur_level > 0:
                for item in self.packages_depencies[cur_package].items():
                    if not item in visited:
                        visited.append(item)
                        queue.append((item, cur_level-1))
                        depencies.append((cur_package, item))
        return depencies
    





keys = ["package_name", "url", "mode_test_dir", "file_name_graph", "mode_output"]
file = "temp.xml"
value = "value"
# tree = ET.parse(file)
# for key in keys:
#     print(f"{key} : {get_value(tree, key)}")

package_parser = Package_parser("packages")
graph_manager = Graph_manager(package_parser)
graphviz = Graphviz_manager()

test_depencies = [(('c', '0.7.0'), ('base', '1.2.0')), (('c', '0.7.0'), ('a', '0.2.0')), (('a', '0.2.0'), ('base', '1.0.0'))]
graphviz.create_graph("Graph", test_depencies)
print(graph_manager.get_array_dependecies_from_package_to_level('c', '0.7.0', 3))


# tree = ET.parse(file)
# for key in keys:
#     print(f"{key} : {get_value(tree, key)}")


