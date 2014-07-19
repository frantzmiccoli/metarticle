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

    def prepare_communities(self):
        self.dendrogram = community.generate_dendrogram(self.g)
        for level in range(len(self.dendrogram)) :
            print "partition at level", level, "is",\
                community.partition_at_level(self.dendrogram, level)

    def get_communities_levels_number(self):
        return len(self.dendrogram)

    def get_communities_level(self, level, relevant_entities=None):
        communities_main_entities = {}
        partition = community.partition_at_level(self.dendrogram, level)

        for entity, partition_code in partition.iteritems():
            if (relevant_entities is not None) and\
                    (entity not in relevant_entities):
                continue
            if partition_code not in communities_main_entities:
                communities_main_entities[partition_code] = entity
            else:
                new_entity_weight = self._get_weight(entity)
                current_entity = communities_main_entities[partition_code]
                current_entity_weight = self._get_weight(current_entity)
                if current_entity_weight < new_entity_weight:
                    communities_main_entities[partition_code] = entity
        return communities_main_entities

    def get_covered_entities(self, entity, level):
        partition = community.partition_at_level(self.dendrogram, level)
        interesting_partition_code = partition[entity]
        covered_entities = []
        for entity, partition_code in partition.iteritems():
            if partition_code != interesting_partition_code:
                continue
            covered_entities.append(entity)
        return covered_entities

    def _get_weight(self, entity):
        total = 0.0
        for neighbor in self.g[entity].viewkeys():
            edge = self.g[entity][neighbor]
            weight = edge['weight']
            total += weight
        return total


if __name__ == '__main__':
    test_graph = ConceptGraph()
    test_graph.add_edge('frite', 'huile')
    test_graph.add_edge('frite', 'ketchup')
    test_graph.add_edge('frite', 'burger')
    test_graph.add_edge('frite', 'burger')
    test_graph.add_edge('ketchup', 'burger')
    test_graph.add_edge('cornichon', 'burger')
    test_graph.add_edge('cornichon', 'concombre')
    test_graph.add_edge('legume', 'concombre')
    test_graph.add_edge('legume', 'cornichon')
    test_graph.add_edge('legume', 'olive')
    test_graph.add_edge('olive', 'huile')
    test_graph.add_edge('huile', 'tournesol')
    test_graph.add_edge('burger', 'mcdo')
    test_graph.add_edge('burger', 'quick')
    test_graph.add_edge('mcdo', 'restaurant')
    test_graph.add_edge('quick', 'restaurant')
    test_graph.add_edge('ketchup', 'rouge')
    test_graph.add_edge('mcdo', 'rouge')
    test_graph.add_edge('quick', 'rouge')
    test_graph.add_edge('quick', 'belge')
    test_graph.add_edge('frite', 'belge')
    test_graph.add_edge('mcdo', 'americain')
    test_graph.add_edge('OGM', 'americain')
    test_graph.add_edge('OGM', 'legume')
    test_graph.add_edge('belge', 'biere')
    test_graph.add_edge('americain', 'biere')

    test_graph.prepare_communities()
    print test_graph.get_communities_level(1)
    print test_graph.get_covered_entities('biere', 1)