from nltk.corpus import wordnet2021 as wn
from collections import defaultdict
from parts_of_speech.wordnet_pos_mapping import DICTIONARY_PARTS_OF_SPEECH_TO_WORDNET_PARTS_OF_SPEECH, IGNORE

Word = str
Lemma = str
Definition = str
UniversalPOS = str
WordnetPOS = str


class Lemmatizer:
    _wn = wn
    _MORPHOLOGICAL_SUBSTITUTIONS: dict[str, list] = wn.MORPHOLOGICAL_SUBSTITUTIONS
    _EXCEPTIONS_MAP: dict[WordnetPOS, dict[Word, Lemma]] = wn._exception_map

    def __init__(self, dictionary: dict[str, dict[str, str]]):
        self.__dictionary: dict[str, set[str]] = self.__simplify_dictionary(dictionary)

    def __simplify_dictionary(self, dictionary: dict[str, dict[str, str]]) -> dict[str, set[str]]:
        simplified_dictionary = dict()
        for word in dictionary:
            wn_poses = set()
            uposes = set(dictionary[word].keys())
            for upos in uposes:
                for wordnet_poses in DICTIONARY_PARTS_OF_SPEECH_TO_WORDNET_PARTS_OF_SPEECH[upos]:
                    wn_poses.update(wordnet_poses)
            simplified_dictionary[word] = wn_poses
        return simplified_dictionary

    def lemmatize_words(
        self, words_to_uposes: dict[Word, set[UniversalPOS]]
    ) -> dict[Lemma, set[UniversalPOS]]:
        lemmas_to_uposes = defaultdict(set)
        for word in words_to_uposes:
            for dpos in words_to_uposes[word]:
                lemmas = self.lemmatize(word, dpos)
                if lemmas:
                    for lemma in lemmas:
                        lemmas_to_uposes[lemma].add(dpos)
        return lemmas_to_uposes

    # all lemmas that match
    # returns None if word does not allow itself to be lemmatized
    # returns empty set if no lemma is found
    def lemmatize(self, word: Word, upos: UniversalPOS) -> set[Lemma]:
        if upos not in DICTIONARY_PARTS_OF_SPEECH_TO_WORDNET_PARTS_OF_SPEECH:
            return None

        wordnet_poses: set[str] = DICTIONARY_PARTS_OF_SPEECH_TO_WORDNET_PARTS_OF_SPEECH[upos]
        if wordnet_poses == IGNORE:
            return None

        return self.__all_lemmas(word, wordnet_poses)

    def __all_lemmas(self, word: Word, wordnet_poses: set[WordnetPOS]) -> set[Lemma]:
        return {
            lemma
            for wordnet_pos in wordnet_poses
            for lemma in self.__lemmatize_for_single_wordnet_pos(word, wordnet_pos)
            if lemma
        }

    def __lemmatize_for_single_wordnet_pos(
        self, word: Word, wordnet_pos: WordnetPOS
    ) -> set[Lemma]:
        if self.__is_exceptional(word, wordnet_pos):
            return set(self.__get_exception(word, wordnet_pos))
        return self.__repeatedly_apply_rules(word, wordnet_pos)

    def __is_exceptional(self, word: Word, wordnet_pos: WordnetPOS) -> bool:
        return (
            wordnet_pos in self._EXCEPTIONS_MAP
            and word in self._EXCEPTIONS_MAP[wordnet_pos]
        )

    def __get_exception(self, word: Word, wordnet_pos: WordnetPOS) -> Lemma:
        return self._EXCEPTIONS_MAP[wordnet_pos][word]

    def __apply_substitution_rules(
        self, forms: set[str], wordnet_pos: str
    ) -> list[str]:
        return [
            form[: -len(old)] + new
            for form in forms
            for old, new in Lemmatizer._MORPHOLOGICAL_SUBSTITUTIONS[wordnet_pos]
            if form.endswith(old)
        ]
    
    def __lemmas_from_vocabulary(self, words: set[str], wordnet_pos: str) -> set[str]:
        return { word for word in words if word in self.__dictionary and wordnet_pos in self.__dictionary[word] }

    def __repeatedly_apply_rules(self, word: str, wordnet_pos: str) -> set[str]:
        forms = {word}
        lemmas = set()
        seen = set()

        # while there are still unseen forms left
        while forms:

            # mark the new forms as being seen
            seen.update(forms)

            # check for lemmas in the new forms
            new_lemmas = self.__lemmas_from_vocabulary(forms, wordnet_pos)
            lemmas.update(new_lemmas)

            # apply the transformative rules
            new_forms: set[str] = self.__apply_substitution_rules(forms, wordnet_pos)
            
            # filter the forms that have already been seen
            filtered_new_forms = [new_form for new_form in new_forms if new_form not in seen]

            # the new forms that have not been seen become the new "forms" set
            forms = filtered_new_forms

        # return the lemmas
        return lemmas
