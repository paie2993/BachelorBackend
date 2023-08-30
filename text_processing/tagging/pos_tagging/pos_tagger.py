import nltk


class Tagger:
    def __init__(self):
        self._tagger = nltk.PerceptronTagger()

    def train(self, train_data, filename):
        self._tagger.train(train_data, save_loc=filename)

    def load(self, filename):
        self._tagger.load(filename)

    def accuracy(self, test_data):
        return self._tagger.accuracy(test_data)

    def tag_word(self, word: str):
        return self._tagger.tag([word])[0]

    def tag_sent(self, words: list[str]) -> list[tuple[str, str]]:
        return self._tagger.tag(words)

    def tag_sents(self, sents: list[list[str]]):
        return [self.tag_sent(sent) for sent in sents]
