from resources.preconditions.environment.environment import hyphenation_pattern
from text_processing.tagging.pos_tagging.pos_tagger import Tagger


class HyphenedFeatureExtractor:
    def __init__(self, pos_tagger: Tagger):
        self._pos_tagger = pos_tagger

    def get_features(self, hyphenation: str) -> dict:
        tagged_components = self.__tagged_components(hyphenation)
        number_components = len(tagged_components)
        features = dict()
        features["len"] = number_components
        features["matches-structure"] = self.__matches_hyphenation_pattern(hyphenation)
        for i in range(number_components):
            features[f"{i}-pos"] = tagged_components[i][1]
        return features

    def __matches_hyphenation_pattern(self, hyphenation: str) -> bool:
        return bool(hyphenation_pattern.fullmatch(hyphenation))

    def __tagged_components(self, hyphenation: str) -> list[tuple[str, str]]:
        components = self.__hyphenation_components(hyphenation)
        return self.__tag_components(components)

    def __hyphenation_components(self, hyphenation: str) -> list[str]:
        return hyphenation.split("-")

    def __tag_components(
        self, hyphenation_components: list[str]
    ) -> list[tuple[str, str]]:
        return self._pos_tagger.tag_sent(hyphenation_components)
