import re

from ..expander.expander import Expander
from ..hyphened.hyphened import HyphenedWordClassifier
from nltk.tokenize import RegexpTokenizer


class Tokenizer:
    _tokenizer = RegexpTokenizer(
        r'(?:\'?(?:\w+\'?)+#\'?(?:\w+\'?)+)+|[][)(}{\'\-.,!?:;"*$&]+|\w+'
    )  # simple words | hyphened words | punctuation characters
    _expander = Expander()

    _hyphenation_regex = r"(?:\'?(?:\w+\'?)+-\'?(?:\w+\'?)+)+"
    _hyphenation_pattern = re.compile(_hyphenation_regex)

    def __init__(self, hyphened_word_classifier):
        self._hyphened_word_classifier: HyphenedWordClassifier = (
            hyphened_word_classifier
        )

    def tokenize(self, raw_text: str) -> list[str]:
        # remove newlines
        raw_text = self.remove_extra_space_characters(raw_text)

        # expand the contractions
        raw_text = self.expand_contractions(raw_text)

        # mark the hyphened words
        raw_text = self.mark_hyphened_words(raw_text)

        # lowercase
        raw_text = raw_text.lower()

        # tokenize the text by regex
        tokens: list[str] = self._tokenizer.tokenize(raw_text)

        # unmark hyphened words
        tokens = list(map(self.unmark_hyphened_word, tokens))

        return tokens

    def remove_extra_space_characters(self, text):
        return re.sub(r"\s+", " ", text)

    def expand_contractions(self, text):
        return self._expander.expand_contractions(text)

    def mark_hyphened_words(self, text):
        hyphenations = self.find_all_hyphenations_words(text)
        hyphened_words = [
            h
            for h in hyphenations
            if self._hyphened_word_classifier.is_hyphened_word(h)
        ]
        for h in hyphened_words:
            substitution = self.hyphened_word_substitution(h)
            text = re.sub(h, substitution, text)
        return text

    def find_all_hyphenations_words(self, text: str) -> list[str]:
        return self._hyphenation_pattern.findall(text)

    def hyphened_word_substitution(self, word):
        re.sub(r"-", "#", word)

    def unmark_hyphened_word(self, word: str) -> str:
        return re.sub(r"#", "-", word)
