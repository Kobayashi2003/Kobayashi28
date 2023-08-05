import gc

class TreeNode:
    def __init__(self, parent=None):
        self.left = None
        self.right = None
        self.parent = parent

node1 = TreeNode()
node2 = TreeNode(node1)
node1.left = node2

del node1
del node2

print(gc.collect())