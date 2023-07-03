import spacy


class NLPModelLoader:
    """Class to load and manage NLP models."""

    def __init__(self):
        self.models = {}

    def load_model(self, model_name):
        """Load an NLP model and store it in the models dictionary."""
        if model_name not in self.models:
            nlp = spacy.load(model_name, disable=["ner", "parser", "textcat", "entity_linker", "tagger"])
            print("NLP Spacy Model " + nlp.meta["lang"] + "_" + nlp.meta["name"] + " is loading...")
            self.models[model_name] = nlp
        return self.models[model_name]

    def get_model(self, model_name):
        """Get an NLP model from the models dictionary."""
        if model_name in self.models:
            return self.models[model_name]
        else:
            raise ValueError(f"Model {model_name} not loaded.")
