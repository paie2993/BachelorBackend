from .univeral_pos import *



DICTIONARY_MAPPING = {
    "noun" : NOUN,
    "pl n": NOUN,
    "verb" : VERB,
    "verb phrases" : VERB,
    "auxiliary verb" : VERB,
    "verb (used with object)" : VERB,
    "verb (used without object)" : VERB,
    "adverb" : ADVERB,
    "adjective" : ADJECTIVE,
    "conjunction" : CONJUNCTION,
    "pronoun" : PRONOUN,
    "interjection" : OTHER,
}

# maps from dictionary.com parts-of-speech to universal parts-of-speech
class OnlineDictionaryPOSAdapter:

    def dictionary_pos_to_universal_pos(self, dpos: str) -> str:
        dpos = dpos.strip(' .,')
        dpos = dpos.lower()
        if dpos not in DICTIONARY_MAPPING:
            return OTHER
        return DICTIONARY_MAPPING[dpos]


