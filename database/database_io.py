import json
from redis import Redis

from resources.preconditions.environment.environment import (
    DICTIONARY_COLLECTION_NAME,
    HYPHENED_WORD_COLLECTION_NAME,
    INVALID_HYPHENATIONS_COLLECTION_NAME,
    USER_DICTIONARY_COLLECTION_NAME,
    USER_VOCABULARY_COLLECTION_NAME,
    VOCABULARY_COLLECTION_NAME,
)


class DatabaseIO:
    def __init__(self):
        self.__connection: Redis

    def open(self, host, port, db):
        self.__connection = Redis(
            host=host,
            port=port,
            db=db,
            charset="utf-8",
            decode_responses=True,
        )

    def close(self):
        self.__connection.close()

    # load
    def load_vocabulary(self):
        return self.__load_named_vocabulary(VOCABULARY_COLLECTION_NAME)

    def load_dictionary(self) -> dict[str, dict[str, list[str]]]:
        return self.__load_named_dictionary(DICTIONARY_COLLECTION_NAME)

    def load_user_vocabulary(self):
        return self.__load_named_vocabulary(USER_VOCABULARY_COLLECTION_NAME)

    def load_user_dictionary(self):
        return self.__load_named_dictionary(USER_DICTIONARY_COLLECTION_NAME)

    def load_hyphened(self):
        return self.__load_named_vocabulary(HYPHENED_WORD_COLLECTION_NAME)

    def load_invalid_hyphened(self):
        return self.__load_named_vocabulary(INVALID_HYPHENATIONS_COLLECTION_NAME)

    def __load_named_dictionary(self, name):
        serialized_dictionary: dict[str, str] = self.__connection.hgetall(name)
        dictionary = {
            key: json.loads(value) for key, value in serialized_dictionary.items()
        }
        return dictionary

    def __load_named_vocabulary(self, name):
        return set(self.__connection.smembers(name))

    # set
    def set_dictionary(self, dictionary: dict):
        self.__set_named_dictionary(DICTIONARY_COLLECTION_NAME, dictionary)

    def set_user_dictionary(self, dictionary: dict):
        self.__set_named_dictionary(USER_DICTIONARY_COLLECTION_NAME, dictionary)

    def __set_named_dictionary(self, name, dictionary):
        serialized_dict = {key: json.dumps(value) for key, value in dictionary.items()}
        self.__connection.delete(name)
        self.__connection.hset(name, mapping=serialized_dict)

    # update
    def update_dictionary(self, dictionary):
        self.__update_named_dictionary(DICTIONARY_COLLECTION_NAME, dictionary)

    def update_user_dictionary(self, dictionary):
        self.__update_named_dictionary(USER_DICTIONARY_COLLECTION_NAME, dictionary)

    def __update_named_dictionary(self, name, dictionary):
        serialized_dict = {key: json.dumps(value) for key, value in dictionary.items()}
        self.__connection.hset(name, mapping=serialized_dict)

    # add
    def add_word_to_user_dictionary(self, word):
        serialized_definitions = self.__connection.hget(DICTIONARY_COLLECTION_NAME, word)
        self.__connection.hset(USER_DICTIONARY_COLLECTION_NAME, word, serialized_definitions)

    # remove collections
    def remove_dictionary(self):
        self.__remove_named_collection(DICTIONARY_COLLECTION_NAME)

    def remove_user_dictionary(self):
        self.__remove_named_collection(USER_DICTIONARY_COLLECTION_NAME)

    def remove_vocabulary(self):
        self.__remove_named_collection(VOCABULARY_COLLECTION_NAME)

    def remove_user_vocabulary(self):
        self.__remove_named_collection(USER_VOCABULARY_COLLECTION_NAME)

    def __remove_named_collection(self, name):
        self.__connection.delete(name)

    def remove_definitions_from_dictionary(self, words: list):
        self.__remove_definitions_from_named_dictionary(
            DICTIONARY_COLLECTION_NAME, words
        )

    # remove definitions
    def remove_definitions_from_user_dictionary(self, words: list[str]):
        self.__remove_definitions_from_named_dictionary(
            USER_DICTIONARY_COLLECTION_NAME, words
        )

    def __remove_definitions_from_named_dictionary(self, name, words: list[str]):
        self.__connection.hdel(name, *words)
