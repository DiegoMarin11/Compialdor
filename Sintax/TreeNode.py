class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []  # Se puede tener varios hijos por algunas producciones

    def add_child(self, node):
        self.children.append(node)

    def print_productions(self):
      
        print(self.value)
        for child in self.children:
            child.print_productions()
