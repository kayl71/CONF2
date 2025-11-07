import xml.etree.ElementTree as ET
def change_value(tree, key, new_value):
    for name in tree.findall(".//" + key):
        name.text = new_value
    ET.dump(tree)
    
def add_value(tree, key, value):
    tree.getroot().set(key, value)
    ET.dump(tree)

def get_value(tree, key):
    finded_tags = tree.findall(".//"+key)
    if len(finded_tags) > 0:
        return finded_tags[0].text
    return None

keys = ["package_name", "url", "mode_test_dir", "file_name_graph", "mode_output"]
file = "temp.xml"
value = "value"
tree = ET.parse(file)
for key in keys:
    print(f"{key} : {get_value(tree, key)}")