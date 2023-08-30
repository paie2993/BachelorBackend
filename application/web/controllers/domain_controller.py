import nltk
from data_structures.aggregators.aggregator import Aggregator
from database.database_io import DatabaseIO
from resources.preconditions.environment.environment import *
from text_processing.lemmatization.lemmatizer import Lemmatizer
from text_processing.sentence.sentence_segmenter import SentenceSegmenter
from parts_of_speech.pos_mapper import TagMapper
from text_processing.tagging.pos_tagging.pos_tagger import Tagger
from text_processing.tokenization.tokenizer import Tokenizer


class DomainController:
    def __init__(
        self,
        data: DatabaseIO,
        segmenter: SentenceSegmenter,
        tokenizer: Tokenizer,
        tagger: Tagger,
        tag_mapper: TagMapper,
        aggregator: Aggregator,
        lemmatizer: Lemmatizer,
    ):
        self.__data = data
        self.__segmenter = segmenter
        self.__tokenizer = tokenizer
        self.__tagger = tagger
        self.__tag_mapper = tag_mapper
        self.__aggregator = aggregator
        self.__lemmatizer = lemmatizer

    # get
    def get_vocabulary(self) -> list[str]:
        return list(self.__data.load_vocabulary())

    def get_dictionary(self):
        return self.__data.load_dictionary()

    def get_user_vocabulary(self) -> list[str]:
        return self.__data.load_user_vocabulary()

    def get_user_dictionary(self, ) -> dict[str, dict[str, str]]:
        return self.__data.load_user_dictionary()

    def get_hyphened(self) -> list[str]:
        return list(self.__data.load_hyphened())

    def get_invalid_hyphened(self) -> list[str]:
        return list(self.__data.load_invalid_hyphened())

    # update
    def update_user_dictionary(self, word: str, pos: str):
        dictionary = self.__data.load_dictionary()
        definitions = dictionary[word][pos]
        dictionary_update = { word: { pos: definitions } }
        self.__data.update_user_dictionary(dictionary_update)

    # add
    def add_word_to_user_dictionary(self, word):
        self.__data.add_word_to_user_dictionary(word)

    # remove definitions
    def remove_definitions_from_user_dictionary(self, words: list[str]):
        self.__data.remove_definitions_from_user_dictionary(words)

    # nlp workflows
    def from_raw_to_sentenced(self, text: str):
        return self.__get_sentences(text)

    def from_raw_to_tokenized_sentences(self, text: str):
        sents = self.from_raw_to_sentenced(text)
        return self.__get_tokenized_sentences(sents)

    def from_raw_to_tagged_sentences(self, text: str):
        tokenized_sents = self.from_raw_to_tokenized_sentences(text)
        return self.__get_tagged_sentences(tokenized_sents)

    def from_raw_to_universal_tagged_sentences(self, text: str):
        tagged_sents = self.from_raw_to_tagged_sentences(text)
        return self.__get_universal_tagged_sentences(tagged_sents)

    def from_raw_to_lemmas(self, text: str):
        universal_tagged_sentences = self.from_raw_to_universal_tagged_sentences(text)
        return self.__get_lemmas(universal_tagged_sentences)

    def from_raw_to_definitions(self, text: str):
        lemmas_to_universal_poses = self.from_raw_to_lemmas(text)
        user_dictionary = self.get_user_dictionary()
        filtered = { lemma: uposes for lemma, uposes in lemmas_to_universal_poses.items() if lemma not in user_dictionary }
        print(f"Found lemmas: {len(lemmas_to_universal_poses)}")
        print(f"Lemmas kept after filtering: {len(filtered)}")
        return self.__get_definitions(filtered)

    def from_title_to_definitions(self, title: str):
        raw_text = nltk.corpus.gutenberg.raw(title)
        return self.from_raw_to_definitions(raw_text)

    # nlp intermediary steps
    def __get_sentences(self, text: str) -> list[str]:
        return self.__segmenter.segment(text)

    def __get_tokenized_sentences(self, sents: list[str]) -> list[list[str]]:
        return [self.__tokenizer.tokenize(sent) for sent in sents]

    def __get_tagged_sentences(
        self,
        tokenized_sents: list[list[str]],
    ) -> list[list[tuple[str, str]]]:
        return self.__tagger.tag_sents(tokenized_sents)

    def __get_universal_tagged_sentences(
        self, tagged_sents: list[list[tuple[str, str]]]
    ) -> list[list[tuple[str, str]]]:
        return self.__tag_mapper.map_sents_with_tags(tagged_sents)

    def __get_lemmas(
        self, universal_tagged_sents: list[list[tuple[str, str]]]
    ) -> dict[str, set[str]]:
        flattened: list = self.__aggregator.flatten(universal_tagged_sents)
        aggregated_by_word: dict[
            str, set[str]
        ] = self.__aggregator.aggregate_by_second_value(flattened)
        return self.__lemmatizer.lemmatize_words(aggregated_by_word)

    def __get_definitions(self, lemmas_to_universal_poses: dict[str, set[str]]):
        dictionary: dict[str, dict[str, str]] = self.get_dictionary()
        return self.__aggregator.intersect(dictionary, lemmas_to_universal_poses)
