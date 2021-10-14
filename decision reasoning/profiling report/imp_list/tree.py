class TreeNode(object):
    def __init__(self, file, name, state, action):
        self.file = file
        self.name = name
        self.state = state
        self.action = action
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

    def add_child_to(self, name, new_node):
        target_node = self.find_name(name)
        target_node.add_child(new_node)

    def find_name(self, name):
        found_node = None
        # init node
        if self.name == name:
            return self
        # else
        for child_node in self.children:
            if child_node.name == name:
                return child_node
            found_node = child_node.find_name(name)
            # leaf node
            if found_node != None:
                return found_node
    
    def find_state(self, state):
        found_node = None
        # init node
        if self.state == state:
            return self
        # else
        for child_node in self.children:
            if child_node.state == state:
                return child_node
            found_node = child_node.find_state(state)
            # leaf node
            if found_node != None:
                return found_node

    def update_state(self, name):
        if len(self.children) == 3:
            if self.name == name:
                self.state = 'current'
            else:
                self.state = 'true'
            for child in self.children:
                child.update_state(name)
        else:
            if self.state == '':
                self.state = 'recommend'
            else:
                self.state = 'false'
        return self

    def dict_to_tree(self, child_node_list):
        for child_node in child_node_list:
            new_node = TreeNode(file = child_node['file'], name = child_node['name'], state = child_node['state'], action = child_node['action'])
            new_node = new_node.dict_to_tree(child_node['children'])
            self.add_child(new_node)
        return self

    def tree_to_dict(self):
        tree_dict = dict()
        children = []
        for child in self.children:
            child_dict = child.tree_to_dict()
            children.append(child_dict)
        tree_dict.update({'file': self.file, 'name': self.name, 'state': self.state, 'action': self.action, 'children': children})
        return tree_dict