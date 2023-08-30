FROM python:latest

RUN ["pip3", "install", "redis"]
RUN ["pip3", "install", "nltk"]
RUN ["pip3", "install", "bs4"]
RUN ["pip3", "install", "flask"]
RUN ["pip3", "install", "flask_cors"]
RUN ["pip3", "install", "pymple"]
RUN ["pip3", "install", "numpy"]

COPY ["./resources/preconditions/nltk_init/", "/app/resources/preconditions/nltk_init/"]

WORKDIR /app/resources/preconditions/nltk_init/

RUN ["python3", "-m", "nltk_init"]

WORKDIR /app/

ENV POS_TAGGER_FILENAME=/dynamic_resources/pos_tagger.pickle                                \
    HYPHENED_WORD_CLASSIFIER_FILENAME=/dynamic_resources/hyphened_word_classifier.pickle    \
    DATABASE_HOST=localhost                                                                 \
    DATABASE_PORT=6379                                                                      \
    DATABASE_NAME=0                                                                         \
    HYPHENED_WORD_COLLECTION_NAME=hyphened                                                  \
    INVALID_HYPHENATIONS_COLLECTION_NAME=invalid_hyphened                                   \
    DICTIONARY_COLLECTION_NAME=dictionary                                                   \
    VOCABULARY_COLLECTION_NAME=vocabulary                                                   \
    USER_DICTIONARY_COLLECTION_NAME=user_dictionary                                         \
    USER_VOCABULARY_COLLECTION_NAME=user_vocabulary                                         \
    FLASK_APP=/app/entrypoint.py

EXPOSE 5000

ENTRYPOINT ["flask", "run"]

CMD ["--host", "0.0.0.0"]

COPY ["./", "/app/"]