"""
This package format the output for D3
"""

def get_d3_representation(concept_graph):
    representation = {
        "name": "Node",
        "children": get_d3_children_representation(concept_graph)
    }
    return enhance_d3_representation(representation)


def get_d3_children_representation(concept_graph,
                                   filtered_entities=None,
                                   level_from_top=1):
    level = concept_graph.get_communities_levels_number() - level_from_top
    if level < 0:
        return get_d3_flat_representation(concept_graph, filtered_entities)

    representation = []
    communities = concept_graph.get_communities_level(level, filtered_entities)

    for _, entity_label in communities .iteritems():
        community_representation = {"name": entity_label}
        community_entities = concept_graph.get_covered_entities(entity_label,
                                                                level)

        if len(community_entities) == 1:
            size = concept_graph.get_weight(entity_label)
            community_representation["value"] = size
        else:
            community_representation["children"] = \
                get_d3_children_representation(concept_graph,
                                               community_entities,
                                               level_from_top + 1)
        representation.append(community_representation)

    return representation


def get_d3_flat_representation(concept_graph, entities):
    representation = []
    for entity in entities:
        representation.append({
            "name": entity,
            "value": concept_graph.get_weight(entity)
        })
    return representation


def enhance_d3_representation(representation):
    """
    Currently some elements can contain only one children which doesn't make
    sense. Let's fix this.

    :param representation:dict
    :return:
    """
    if not representation.has_key('children'):
        #Leaf node nothing to do
        return
    if len(representation['children']) == 1:
        representation['children'] = representation['children'][0]['children']
        enhance_d3_representation(representation)
        return
    for child in representation['children']:
        enhance_d3_representation(child)