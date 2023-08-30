import nltk
from data_structures.aggregators.aggregator import Aggregator

from dictionary.seed.seed import DictionarySeeder
from text_processing.sentence.sentence_segmenter import SentenceSegmenter
from text_processing.tokenization.tokenizer import Tokenizer


class ControlController:
    pass

    def __init__(
        self,
        seeder: DictionarySeeder,
        segmenter: SentenceSegmenter,
        tokenizer: Tokenizer,
        aggregator: Aggregator,
    ):
        self.__seeder = seeder
        self.__segmenter = segmenter
        self.__tokenizer = tokenizer
        self.__aggregator = aggregator

    def seed_dictionary_with_raw_text(self, text: str):
        unique_words = self.__get_words_from_raw_text(text)
        self.__seeder.seed_dictionary_with_specific_words(unique_words)

    def seed_dictionary_with_text_by_name(self, name: str):
        unique_words = self.__get_text_words(name)
        self.__seeder.seed_dictionary_with_specific_words(unique_words)

    def seed_dictionary_with_random_words(self, count: int):
        self.__seeder.seed_dictionary_with_random_words(count)

    def __get_text_words(self, name: str) -> set[str]:
        return set(nltk.corpus.gutenberg.words(name))

    def __get_words_from_raw_text(self, text: str) -> set[str]:
        sents = self.__segmenter.segment(text)
        tokenized_sents = list(map(lambda sent: self.__tokenizer.tokenize(sent), sents))
        return str(self.__aggregator.flatten(tokenized_sents))
