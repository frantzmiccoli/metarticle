import itertools

import crawler
import entity
import context
import sentiment
import conceptgraph


target_url = 'http://www.cbinsights.com/blog/startup-failure-post-mortem'

texts = crawler.get_texts_from_url(target_url)

resolved_texts = [entity.resolve_anaphores(text) for text in texts]

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
        entities.append(extracted_entity)
        if extracted_entity not in entities_sentiments:
            entities_sentiments[extracted_entity] = []
        entities_sentiments[extracted_entity].append(entity_sentiment)

    for (entity1, entity2) in itertools.combinations(context_entities_set, 2):
        concept_graph.add_edge(entity1, entity2)

concept_graph.prepare_communities()


