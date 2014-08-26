import itertools

import crawler
import entity
import context
import sentiment
import conceptgraph
import domainexcludedentities

#target_url = 'http://www.cbinsights.com/blog/startup-failure-post-mortem'
target_url = 'https://api.github.com/search/repositories?q=node+language:javascript&sort=stars&order=desc&per_page=100'

def compute_sentiment(entity_sentiments):
    counters = {}
    for sentiment in entity_sentiments:
        if sentiment in counters:
            counters[sentiment] += 1
        else:
            counters[sentiment] = 1

    best, best_count = 'neutral', 0
    total = 0
    for sentiment, value_count in counters.items():
        total += value_count
        if value_count > best_count:
            best = sentiment
            best_count = value_count

    return best, float(best_count)/float(total)


def get_d3_representation(concept_graph):
    representation = {
        "name": "Node",
        "children": get_d3_children_representation(concept_graph)
    }
    return representation


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


'''Cache util'''
import os
import cacheutil
cache_dir_path = '../data/inferred'
cacheutil.ensure_accessible_cache_dir(cache_dir_path)

entities_cache_path = os.path.join(cache_dir_path, 'entities')
entities = cacheutil.get_from_cache(entities_cache_path)

entities_sentiments_cache_path = os.path.join(cache_dir_path, 'entities_sentiments')
entities_sentiments = cacheutil.get_from_cache(entities_sentiments_cache_path)

concept_graph_cache_path = os.path.join(cache_dir_path, 'concept_graph')
concept_graph = cacheutil.get_from_cache(concept_graph_cache_path)

level_cache_path = os.path.join(cache_dir_path, 'level')
level = cacheutil.get_from_cache(level_cache_path)

communities_cache_path = os.path.join(cache_dir_path, 'communities')
communities = cacheutil.get_from_cache(communities_cache_path)


if concept_graph is None:
    texts = crawler.get_texts_from_url(target_url)

    resolved_texts = [entity.resolve_anaphores(text) for text in texts]

    domain_excluded_entities = domainexcludedentities.\
        get_domain_excluded_entities(texts)

    contexts_lists = [context.extract(text) for text in texts]
    contexts = []
    for contexts_list in contexts_lists:
        contexts += contexts_list

    entities = []
    entities_sentiments = {}
    concept_graph = conceptgraph.ConceptGraph()
    for candidate_context in contexts:
        entity_sentiment = sentiment.get_sentiment(candidate_context)
        context_entities_set = set(entity.extract(candidate_context))
        for extracted_entity in context_entities_set:
            if extracted_entity in domain_excluded_entities:
                continue
            entities.append(extracted_entity)
            if extracted_entity not in entities_sentiments:
                entities_sentiments[extracted_entity] = []
            entities_sentiments[extracted_entity].append(entity_sentiment)

        for (entity1, entity2) in itertools.combinations(context_entities_set, 2):
            if (entity1 in domain_excluded_entities) or\
                    (entity2 in domain_excluded_entities):
                continue
            concept_graph.add_edge(entity1, entity2)

    for entity, sentiments in entities_sentiments.iteritems():
        #The length is the number of occurences
        if (len(sentiments) < 10) or (len(sentiments) > 100):
            concept_graph.drop_node(entity)

    concept_graph.prepare_communities()

    cacheutil.store_in_cache(entities_cache_path, entities)
    cacheutil.store_in_cache(entities_sentiments_cache_path,
                             entities_sentiments)
    cacheutil.store_in_cache(concept_graph_cache_path, concept_graph)


d3_representation = get_d3_representation(concept_graph)
enhance_d3_representation(d3_representation)

json_file = open('../public/data.json', 'w')
import json
json_file.write(json.dumps(d3_representation, indent=4))
json_file.flush()
json_file.close()