import nltk
from application.ioc_container.container import container
from application.web.application import create_application
from database.database_io import DatabaseIO
from dictionary.online_dictionary import OnlineDictionary
from dictionary.seed.seed import DictionarySeeder

from random import shuffle

app = create_application()
