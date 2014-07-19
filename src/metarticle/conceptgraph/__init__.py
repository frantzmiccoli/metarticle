import networkx
import community

class ConceptGraph:

    def __init__(self):
        self.g = networkx.Graph()

    def add_edge(self, node1, node2):
        if self.g.has_edge(node1, node2):
            self.g[node1][node2]['weight'] += 1
        else:
            self.g.add_edge(node1, node2, weight=1.0)

    def communities(self):
        #community.best_partition(self.g).values()
        dendrogram = community.generate_dendrogram(self.g)
        for level in range(len(dendrogram) - 1) :
            print "partition at level", level, "is",\
                community.partition_at_level(dendrogram, level)
