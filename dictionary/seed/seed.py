from random import shuffle
from numpy import array_split

from dictionary.online_dictionary import OnlineDictionary
from database.database_io import DatabaseIO
from resources.preconditions.environment.environment import *


class DictionarySeeder:
    __BATCH_SIZE = 25  # arbitrary constant

    def __init__(self, data: DatabaseIO, dictionary: OnlineDictionary):
        self.__data: DatabaseIO = data
        self.__dictionary: OnlineDictionary = dictionary

    def __seed_dictionary(self, words: set[str]):
        batches = array_split(list(words), DictionarySeeder.__BATCH_SIZE)
        for batch in batches:
            definitions: dict[str, dict[str, list[str]]] = self.__dictionary.get_words_definitions(batch)
            self.__data.add_to_dictionary(DICTIONARY_COLLECTION_NAME, definitions)

    def seed_dictionary_with_specific_words(self, words: set[str]):
        self.__seed_dictionary(words)

    def seed_dictionary_with_random_words(self, word_count: int):
        vocabulary: set = self.__data.load_vocabulary(DICTIONARY_COLLECTION_NAME)
        shuffle(vocabulary)
        vocabulary = set(vocabulary[:word_count])
        self.__seed_dictionary(vocabulary)
