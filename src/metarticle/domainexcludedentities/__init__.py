from metarticle import entity

def get_domain_excluded_entities(texts):
    extractor = DomainExcludedEntitiesExtractor(texts)
    return set([entity for entity in extractor.get_excluded_entities()])

class DomainExcludedEntitiesExtractor:

    def __init__(self, texts):
        self.VALID_MIN = 5 / 100
        self.VALID_MAX = 90 / 100
        # {'car': 12} where 12 is the count of text where car has been seen
        self._entities = {}
        self._loaded = 0
        self._set_texts(texts)

    def get_excluded_entities(self):
        for k, v in self._entities.iteritems():
            entity_percentage = float(v) / float(self._loaded)
            if (entity_percentage < self.VALID_MIN) | \
                    (entity_percentage > self.VALID_MAX):
                yield entity

    def _set_texts(self, texts):
        for text in texts:
            self._handle_text(text)

    def _handle_text(self, text):
        concepts = set(entity.extract(text))

        for concept in concepts:
            if concept == 'whodunnit':
                print text
                import sys
                sys.exit()
            if concept not in self._entities:
                self._entities[concept] = 0
            self._entities[concept] += 1
        self._loaded += 1