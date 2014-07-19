import networkx

class ConceptGraph:

    def __init__(self):
        self.g = networkx.Graph()

    def add_edge(self, node1, node2):
        if self.g.has_edge(node1, node2):
            self.g[node1][node2]['weight'] += 1
        else:
            self.g.add_edge(node1, node2, weight=1.0)