class Graph:
    def __init__(self, adj=set()):
        self.adj = adj
    
    def addEdge(self, edge):
        self.adj.add(edge)
    
    def findParent(self, val):
        parent = set()
        for stuff in self.adj:
            if stuff[0] == val:
                parent.add(stuff[1])
        return parent
        
    def print(self):
        return self.adj