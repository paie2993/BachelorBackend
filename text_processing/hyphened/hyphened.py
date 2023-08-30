from .classifier import Classifier
from .extractor import HyphenedFeatureExtractor


class HyphenedWordClassifier:
    def __init__(
        self, feature_extractor: HyphenedFeatureExtractor, classifier: Classifier
    ):
        self.__feature_extractor = feature_extractor
        self.__classifier = classifier

    def is_hyphened_word(self, hyphenation: str) -> bool:
        features = self.__feature_extractor.get_features(hyphenation)
        return self.__classifier.classify(features)
