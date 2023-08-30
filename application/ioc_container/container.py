from pymple import Container
from application.web.controllers.control_controller import ControlController
from application.web.controllers.domain_controller import DomainController
from data_structures.aggregators.aggregator import Aggregator

from database.database_io import DatabaseIO
from dictionary.online_dictionary import OnlineDictionary
from dictionary.seed.seed import DictionarySeeder
from ml_models.models import ModelFiles
from ml_models.trainer import Trainer
from parts_of_speech.online_dictionary_pos_adapter import OnlineDictionaryPOSAdapter
from resources.preconditions.environment.environment import *
from text_processing.hyphened.classifier import Classifier
from text_processing.hyphened.extractor import HyphenedFeatureExtractor
from text_processing.hyphened.hyphened import HyphenedWordClassifier
from text_processing.lemmatization.lemmatizer import Lemmatizer
from text_processing.sentence.sentence_segmenter import SentenceSegmenter
from parts_of_speech.pos_mapper import TagMapper
from text_processing.tagging.pos_tagging.pos_tagger import Tagger
from text_processing.tokenization.tokenizer import Tokenizer


class ContainerIOC:
    def __init__(self):
        self.__container = Container()

    def resolve(self, clazz):
        return self.__container.resolve(clazz)

    def setup_components(self):
        self.__init_all_components()

    def cleanup(self):
        data: DatabaseIO = self.__container.resolve(DatabaseIO)
        data.close()

    def __init_database_connection(self, c: Container) -> DatabaseIO:
        data = DatabaseIO()
        data.open(DATABASE_HOST, DATABASE_PORT, DATABASE_NAME)
        return data

    def __init_model_files(self, c: Container) -> ModelFiles:
        return ModelFiles()

    def __init_sentence_segmenter(self, c: Container) -> SentenceSegmenter:
        return SentenceSegmenter()

    def __init_trainer(self, c: Container) -> Trainer:
        data = c.resolve(DatabaseIO)
        return Trainer(data)

    def __init_hyphened_feature_extractor(
        self, c: Container
    ) -> HyphenedFeatureExtractor:
        tagger = c.resolve(Tagger)
        return HyphenedFeatureExtractor(tagger)

    def __init_classifier(self, c: Container) -> Classifier:
        classifier = Classifier()
        classifier.load(HYPHENED_WORD_CLASSIFIER_FILENAME)
        return classifier

    def __init_hyphened_word_classifier(self, c: Container) -> HyphenedWordClassifier:
        feature_extractor = c.resolve(HyphenedFeatureExtractor)
        classifier = c.resolve(Classifier)
        return HyphenedWordClassifier(feature_extractor, classifier)

    def __init_pos_tagger(self, c: Container) -> Tagger:
        tagger = Tagger()
        tagger.load(POS_TAGGER_FILENAME)
        return tagger

    def __init_tokenizer(self, c: Container) -> Tokenizer:
        hyphened_word_classifier = c.resolve(HyphenedWordClassifier)
        return Tokenizer(hyphened_word_classifier)

    def __init_tag_mapper(self, c: Container) -> TagMapper:
        return TagMapper()

    def __init_lemmatizer(self, c: Container) -> Lemmatizer:
        data: DatabaseIO = c.resolve(DatabaseIO)
        dictionary = data.load_dictionary()
        return Lemmatizer(dictionary)

    def __init_aggregator(self, c: Container) -> Aggregator:
        return Aggregator()

    def __init_dictionary_seeder(self, c: Container) -> DictionarySeeder:
        data: DatabaseIO = c.resolve(DatabaseIO)
        online_dictionary: OnlineDictionary = c.resolve(OnlineDictionary)
        return DictionarySeeder(data, online_dictionary)

    def __init_control_controller(self, c: Container) -> ControlController:
        seeder: DictionarySeeder = c.resolve(DictionarySeeder)
        segmenter: SentenceSegmenter = c.resolve(SentenceSegmenter)
        tokenizer: Tokenizer = c.resolve(Tokenizer)
        aggregator: Aggregator = c.resolve(Aggregator)
        return ControlController(seeder, segmenter, tokenizer, aggregator)

    def __init_domain_controller(self, c: Container) -> DomainController:
        data: DatabaseIO = c.resolve(DatabaseIO)
        segmenter: SentenceSegmenter = c.resolve(SentenceSegmenter)
        tokenizer: Tokenizer = c.resolve(Tokenizer)
        tagger: Tagger = c.resolve(Tagger)
        tag_mapper: TagMapper = c.resolve(TagMapper)
        aggregator: Aggregator = c.resolve(Aggregator)
        lemmatizer: Lemmatizer = c.resolve(Lemmatizer)
        return DomainController(
            data, segmenter, tokenizer, tagger, tag_mapper, aggregator, lemmatizer
        )

    def __init_online_dictionary_pos_adapter(
        self, c: Container
    ) -> OnlineDictionaryPOSAdapter:
        return OnlineDictionaryPOSAdapter()

    def __init_online_dictionary(self, c: Container) -> OnlineDictionary:
        pos_adapter = c.resolve(OnlineDictionaryPOSAdapter)
        return OnlineDictionary(pos_adapter)

    def __init_all_components(self):
        self.__container.register(
            DatabaseIO, lambda c: self.__init_database_connection(c)
        )
        self.__container.register(ModelFiles, lambda c: self.__init_model_files(c))
        self.__container.register(
            SentenceSegmenter, lambda c: self.__init_sentence_segmenter(c)
        )
        self.__container.register(Trainer, lambda c: self.__init_trainer(c))
        self.__container.register(
            HyphenedFeatureExtractor,
            lambda c: self.__init_hyphened_feature_extractor(c),
        )
        self.__container.register(Classifier, lambda c: self.__init_classifier(c))
        self.__container.register(
            HyphenedWordClassifier,
            lambda c: self.__init_hyphened_word_classifier(c),
        )
        self.__container.register(Tokenizer, lambda c: self.__init_tokenizer(c))
        self.__container.register(Tagger, lambda c: self.__init_pos_tagger(c))
        self.__container.register(TagMapper, lambda c: self.__init_tag_mapper(c))
        self.__container.register(Lemmatizer, lambda c: self.__init_lemmatizer(c))
        self.__container.register(Aggregator, lambda c: self.__init_aggregator(c))
        self.__container.register(
            DictionarySeeder, lambda c: self.__init_dictionary_seeder(c)
        )
        self.__container.register(
            ControlController, lambda c: self.__init_control_controller(c)
        )
        self.__container.register(
            DomainController, lambda c: self.__init_domain_controller(c)
        )
        self.__container.register(
            OnlineDictionaryPOSAdapter,
            lambda c: self.__init_online_dictionary_pos_adapter(c),
        )
        self.__container.register(
            OnlineDictionary, lambda c: self.__init_online_dictionary(c)
        )


container = ContainerIOC()
