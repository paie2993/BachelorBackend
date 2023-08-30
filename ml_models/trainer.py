from random import shuffle

from database.database_io import DatabaseIO
from resources.preconditions.environment.environment import *
from text_processing.hyphened.classifier import Classifier
from text_processing.hyphened.extractor import HyphenedFeatureExtractor
from text_processing.tagging.pos_tagging.pos_tagger import Tagger


class Trainer:
    def __init__(self, data: DatabaseIO):
        self._data = data

    def train_pos_tagger(
        self, tagger: Tagger, tagged_sents: list[tuple[str, str]], filename: str
    ):
        tagger.train(tagged_sents, filename)

    def train_hyphenated_word_classifier(
        self,
        feature_extractor: HyphenedFeatureExtractor,
        classifier: Classifier,
        train_data: list[str],
        filename: str,
    ):
        featured_train_data = [
            (feature_extractor.get_features(word), label) for word, label in train_data
        ]
        classifier.train(featured_train_data)
        classifier.store(filename)

    def hyphenated_words_classifier_train_data(self):
        valid = list(self._data.load_vocabulary(HYPHENED_WORD_COLLECTION_NAME))
        shuffle(valid)
        valid = valid[:50]

        invalid = list(self._data.load_vocabulary(INVALID_HYPHENATIONS_COLLECTION_NAME))
        shuffle(invalid)
        invalid = invalid[:50]

        valid_hyphenations = list(map(lambda h: (h, True), valid))
        invalid_hyphenations = list(map(lambda h: (h, False), invalid))

        return valid_hyphenations + invalid_hyphenations

    def train_models(self, tagger, feature_extractor, classifier):
        pos_tagger_train_data = POS_TAGGER_TRAINSET
        classifier_train_data = self.hyphenated_words_classifier_train_data()
        self.train_pos_tagger(tagger, pos_tagger_train_data, POS_TAGGER_FILENAME)
        self.train_hyphenated_word_classifier(
            feature_extractor,
            classifier,
            classifier_train_data,
            HYPHENED_WORD_CLASSIFIER_FILENAME,
        )
