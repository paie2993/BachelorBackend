import re
from bs4 import BeautifulSoup
import urllib
from functools import reduce

from parts_of_speech.online_dictionary_pos_adapter import OnlineDictionaryPOSAdapter

URL = "https://www.dictionary.com/browse"

Word = str
POS = str
Definitions = list[str]


class OnlineDictionary:
    DICTIONARY = "dictionary-site"
    THESAURUS = "thesaurus-site"

    DEFINITIONS_LIMIT = 2

    def __init__(self, pos_adapter: OnlineDictionaryPOSAdapter):
        self.__pos_adapter = pos_adapter

    def get_words_definitions(
        self, words: set[Word]
    ) -> dict[Word, dict[POS, Definitions]]:
        return {
            actual_word: definitions
            for word in words
            for actual_word, definitions in self.get_word_definitions(word).items()
        }

    def get_word_definitions(self, word: str) -> dict[Word, dict[POS, Definitions]]:
        word = word.strip(" ")

        if not word:
            print("Exception: empty string")
            return dict()

        url = f"{URL}/{word}"

        try:
            print(f"Searching: {word}")

            html_doc = self.__get_html_document(url)
            html_tree = self.__get_html_tree(html_doc)

            site_type = self.__resolve_site(html_tree)

            definitions: list
            if site_type:
                definitions = self.__get_definitions(html_tree)
            else:
                definitions = self.__get_synonyms(html_tree)

            print(f"Found: {definitions}")
            return definitions
        except Exception as exception:
            print(f"Exception: {exception}; url: {url}")
            return dict()

    def __get_html_document(self, url):
        return urllib.request.urlopen(url).read()

    def __get_html_tree(self, html_document) -> BeautifulSoup:
        return BeautifulSoup(html_document, "html.parser")

    def __resolve_site(self, soup: BeautifulSoup) -> str:
        dictionary_site = soup.find("div", class_=OnlineDictionary.DICTIONARY)
        if dictionary_site:
            return OnlineDictionary.DICTIONARY
        thesaurus_site = soup.find("div", class_=OnlineDictionary.THESAURUS)
        if thesaurus_site:
            return OnlineDictionary.THESAURUS
        raise Exception("No site found for the request")

    def __get_definitions(self, soup):
        def __get_actual_word(word_definition_card):
            return word_definition_card.find("h1").text.strip()

        def __get_pos(div):
            pos_span = div.find("span", class_=re.compile("pos"))
            dictionary_pos = pos_span.text
            return self.__pos_adapter.dictionary_pos_to_universal_pos(dictionary_pos)

        def __get_definition_for_definition_content_div(div) -> list:
            definition_holders = div.find_all(
                "div", {"data-type": "word-definition-content"}
            )
            definitions_inside_holders = list(
                map(lambda holder: holder.text, definition_holders)
            )[: OnlineDictionary.DEFINITIONS_LIMIT]
            stripped = [definition.strip() for definition in definitions_inside_holders]
            filtered = [definition for definition in stripped if definition]
            return filtered

        word_definition_card = soup.find(
            "section", {"data-type": "word-definition-card"}
        )

        word_definitions_div = word_definition_card.find_all(
            "div", {"data-type": "word-definitions"}
        )

        actual_word = __get_actual_word(word_definition_card)
        pos_definitions_pairs = [
            (__get_pos(div), __get_definition_for_definition_content_div(div))
            for div in word_definitions_div
        ]
        pos_definitions_pairs.reverse()

        return {
            actual_word: {
                pos: definitions for pos, definitions in pos_definitions_pairs
            }
        }

    def __get_synonyms(self, soup):
        def __get_synonyms_card(thesaurus_entry_module):
            return thesaurus_entry_module.find(
                "section", {"data-type": "thesaurus-synonyms-card"}
            )

        def __get_actual_word(thesaurus_entry_module):
            synonyms_card = __get_synonyms_card(thesaurus_entry_module)
            actual_word = synonyms_card.find("em")
            return actual_word.strip()

        def __get_pos_of_first_synonym(thesaurus_entry_module):
            synonyms = __get_synonyms_text(thesaurus_entry_module)
            if not synonyms:
                return None
            first_synonym = synonyms[0]
            first_synonym_definitions = self.get_word_definitions(first_synonym)
            if not first_synonym_definitions:
                return None
            first_synonym_first_definition = first_synonym_definitions[0]
            pos = list(first_synonym_first_definition.keys())[0]
            return pos

        def __get_synonyms_text(thesaurus_entry_module) -> list:
            synonyms_card = __get_synonyms_card(thesaurus_entry_module)
            synonyms_buttons = synonyms_card.find_all(
                "a", {"data-type": "pill-buttons"}
            )
            synonyms_text = [button.text for button in synonyms_buttons][
                : OnlineDictionary.DEFINITIONS_LIMIT
            ]
            return synonyms_text

        def __get_pos(thesaurus_entry_module):
            menu = thesaurus_entry_module.find("menu")
            button = menu.find("button")
            thesaurus_pos = button.find("em")

            if "as in" in thesaurus_pos:
                pos = __get_pos_of_first_synonym(thesaurus_entry_module)
                if pos:
                    return pos

            return thesaurus_pos

        def __get_definition(thesaurus_entry_module):
            synonyms_text = __get_synonyms_text(thesaurus_entry_module)
            stripped = [text.strip() for text in synonyms_text]
            filtered = [text for text in stripped]
            return filtered

        thesaurus_entry_module = soup.find(
            "section", {"data-type": "thesaurus-entry-module"}
        )

        actual_word = __get_actual_word(thesaurus_entry_module)
        pos = __get_pos(thesaurus_entry_module)
        definitions = __get_definition(thesaurus_entry_module)

        if actual_word and pos and definitions:
            return {actual_word: {pos: definitions}}
        return dict()
