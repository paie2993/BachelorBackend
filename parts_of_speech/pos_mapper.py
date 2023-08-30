from parts_of_speech.pos_correspondance import (
    UNIVERSAL_TO_DICTIONARY,
)


class TagMapper:
    def map_sents_with_tags(
        self, sents_with_tags: list[list[tuple[str, str]]]
    ) -> list[list[tuple[str, str]]]:
        return [self.map_tags(sent) for sent in sents_with_tags]

    def map_tags(self, words_and_tags: list[tuple[str, str]]):
        return list(map(lambda t: (t[0], self.__map_tag(t[1])), words_and_tags))

    def __map_tag(self, universal_tag: str) -> str:
        uppercased = universal_tag.upper()
        if universal_tag.upper() in UNIVERSAL_TO_DICTIONARY.keys():
            return UNIVERSAL_TO_DICTIONARY[uppercased]
        else:
            return universal_tag
