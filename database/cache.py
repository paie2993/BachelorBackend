class DatabaseCache:
    def __init__(self):
        self.__dictionary: dict[str, dict[str, list[str]]] = None

    def has_dictionary(self) -> bool:
        return self.__dictionary is not None

    def dictionary(self) -> dict[str, dict[str, list[str]]]:
        return self.__dictionary

    def set_dictionary(self, dictionary):
        self.__dictionary = dictionary

    def invalidate(self):
        self.__dictionary = None
