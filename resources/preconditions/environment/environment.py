import nltk
import os
import re

POS_TAGGER_FILENAME = os.environ["POS_TAGGER_FILENAME"]
HYPHENED_WORD_CLASSIFIER_FILENAME = os.environ["HYPHENED_WORD_CLASSIFIER_FILENAME"]

DATABASE_HOST = os.environ["DATABASE_HOST"]
DATABASE_PORT = os.environ["DATABASE_PORT"]
DATABASE_NAME = os.environ["DATABASE_NAME"]

DICTIONARY_COLLECTION_NAME = os.environ["DICTIONARY_COLLECTION_NAME"]
HYPHENED_WORD_COLLECTION_NAME = os.environ["HYPHENED_WORD_COLLECTION_NAME"]
INVALID_HYPHENATIONS_COLLECTION_NAME = os.environ[
    "INVALID_HYPHENATIONS_COLLECTION_NAME"
]
VOCABULARY_COLLECTION_NAME = os.environ["VOCABULARY_COLLECTION_NAME"]
USER_DICTIONARY_COLLECTION_NAME = os.environ["USER_DICTIONARY_COLLECTION_NAME"]
USER_VOCABULARY_COLLECTION_NAME = os.environ["USER_VOCABULARY_COLLECTION_NAME"]

BUFFER_SIZE = 10000

TAGSET = "universal"
POS_TAGGER_TRAINSET = nltk.corpus.brown.tagged_sents(tagset=TAGSET)[:2000]

hyphenation_pattern = re.compile(r"(\'?(\w+\'?)+-\'?(\w+\'?)+)+")


def default_text():
    return nltk.corpus.gutenberg.raw("carroll-alice.txt")
