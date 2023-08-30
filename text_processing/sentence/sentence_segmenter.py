import nltk

class SentenceSegmenter:

    def segment(self, text):
        return nltk.sent_tokenize(text)