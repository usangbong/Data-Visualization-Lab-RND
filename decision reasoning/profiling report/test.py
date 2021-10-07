import json

class TreeNode(object):
    def __init__(self, file, name, state):
        self.file = file
        self.name = name
        self.state = state
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

    def add_child_to(self, name, new_node):
        target_node = self.find_node(name)
        target_node.add_child(new_node)

    def dict_to_tree(self, child_node_list):
        for child_node in child_node_list:
            new_node = TreeNode(file = child_node['file'], name = child_node['name'], state = child_node['state'])
            new_node = new_node.dict_to_tree(child_node['children'])
            self.add_child(new_node)
        return self

    def find_node(self, name):
        found_node = None
        for child_node in self.children:
            if child_node.name == name:
                return child_node
            found_node = child_node.find_node(name)
        return found_node

    def tree_to_dict(self):
        tree_dict = dict()
        children = []
        for child in self.children:
            child_dict = child.tree_to_dict()
            children.append(child_dict)
        tree_dict.update({'file': self.file, 'name': self.name, 'state': self.state, 'children': children})
        return tree_dict

name = '2'

if __name__ == '__main__':
    with open('static/data/treeData.json') as json_file:
        json_data = json.load(json_file)

    root = TreeNode(file = json_data['file'], name = json_data['name'], state = json_data['state'])
    root = root.dict_to_tree(json_data['children'])

    new_node = TreeNode(file = 'new', name = 'new', state = 'new')
    root.add_child_to('2', new_node)

    output_data = root.tree_to_dict()
    with open('static/data/treeData.json', 'w') as f:
        json.dump(output_data, f, indent = 4)