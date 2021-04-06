# A tree node. Defines some useful methods for trees.
class TreeNode:
    def __init__(self, value, children = None, parent = None):
        # The value of tree
        self.value = value
        # Any children of the tree
        self.children = children or []
        # The parent of the tree if there is any
        self.parent = parent
    # The method literally does what they say, so there are no comments.
    
    def addChild(self, childNode):
        childNode.removeParent()
        self.children.append(childNode)
        childNode.parent = self
    def removeChild(self, childNode):
        assert(childNode in self.children)
        self.children.remove(childNode)
        childNode.parent = None
    def changeParent(self, parentNode):
        parentNode.addChild(self)
    def removeParent(self):
        if self.parent != None:
            self.parent.removeChild(self)
    def getRoot(self):
        root = self
        while root.parent != None:
            root = root.parent
        return root
    def __repr__(self):
        return "{}({} child)".format(self.value, len(self.children))
    def __str__(self):
        returnVal = str(self.value)
        returnVal += "["
        for i in self.children:
            returnVal += str(i) + ","
        returnVal += "]"
        return returnVal

#print(None or 3)