import spacy
from fastcoref import spacy_component

class SpacyModel:
    def __init__(self):
        self.model = spacy.load("en_coreference_web_trf")

    def predict(self, text: str):
        doc = self.model(text)

        offset = 0
        reindex = []
        for chain in doc.spans:
            for idx, span in enumerate(doc.spans[chain]):
                if idx > 0:
                    reindex.append([span.start_char, span.end_char, doc.spans[chain][0].text])

        for span in sorted(reindex, key=lambda x:x[0]):
            text = text[0:span[0] + offset] + span[2] + text[span[1] + offset:]
            offset += len(span[2]) - (span[1] - span[0])
        
        return text

    def __call__(self, text: str):
        return self.predict(text)
    
class FastCoref:
    def __init__(self):
        self.model = spacy.load("en_core_web_sm", exclude=["parser", "lemmatizer", "ner", "textcat"])
        self.model.add_pipe("fastcoref")

    def predict(self, text: str):
        doc = self.model(text, component_cfg={"fastcoref": {'resolve_text': True}})
        return doc._.resolved_text

    def __call__(self, text: str):
        return self.predict(text)