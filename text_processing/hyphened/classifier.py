import nltk
import pickle
from typing import Any


class Classifier:
    def __init__(self):
        self._classifier: nltk.NaiveBayesClassifier

    def store(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self._classifier, f)

    def load(self, filename):
        with open(filename, "rb") as f:
            self._classifier = pickle.load(f)

    def train(self, labeled_features) -> list[tuple[dict[str, Any], bool]]:
        self._classifier = nltk.NaiveBayesClassifier.train(labeled_features)

    def classify(self, features):
        self._classifier.classify(features)
