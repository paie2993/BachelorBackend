from typing import Any
from flask import Blueprint, request
from flask import make_response
from application.web.controllers.domain_controller import DomainController

from application.ioc_container.container import container
from resources.preconditions.environment.environment import *

domain_controller: DomainController = container.resolve(DomainController)

domain = Blueprint("domain", __name__)


def __definitions_to_json(words_pos_definitions: dict[str, dict[str, list]]):
    json_array = []
    for word in words_pos_definitions.keys():
        json = dict()
        json["word"] = word
        json["posDefinitions"]: list[dict] = []
        for pos, definitions in words_pos_definitions[word].items():
            pos_definitions_pair: dict[str, Any] = dict()
            pos_definitions_pair["pos"] = pos
            pos_definitions_pair["definitions"] = definitions
            json["posDefinitions"].append(pos_definitions_pair)
        json_array.append(json)
    return json_array


# get
@domain.route("/vocabulary")
def vocabulary():
    return domain_controller.get_vocabulary()


@domain.route("/dictionary")
def dictionary():
    dictionary = domain_controller.get_dictionary()
    return __definitions_to_json(dictionary)


@domain.route("/user/vocabulary")
def user_vocabulary():
    return domain_controller.get_user_vocabulary()


@domain.route("/user/dictionary")
def user_dictionary():
    user_dictionary = domain_controller.get_user_dictionary()
    return __definitions_to_json(user_dictionary)


@domain.route("/hyphened")
def hyphened():
    return domain_controller.get_hyphened()


@domain.route("/hyphened/invalid")
def invalid_hyphened():
    return domain_controller.get_invalid_hyphened()


# update
@domain.route("/user/dictionary/update/?word=<word>&pos=<pos>")
def user_dictionary_update(word: str, pos: str):
    domain_controller.update_user_dictionary(word, pos)
    return make_response()


# add
@domain.route("/user/dictionary/add/<word>")
def user_dictionary_add_word(word: str):
    domain_controller.add_word_to_user_dictionary(word)
    return make_response()


# remove definitions
@domain.route("/user/dictionary/remove/<word>", methods=["GET"])
def user_dictionary_remove_word(word: str):
    domain_controller.remove_definitions_from_user_dictionary([word])
    return make_response()


@domain.route("/user/dictionary/remove", methods=["POST"])
def user_dictionary_remove_definitions():
    words: list = request.get_json()
    domain_controller.remove_definitions_from_user_dictionary(words)
    return make_response()


# nlp workflows
@domain.route("/text/echo", methods=["POST"])
def echo_text():
    text = request.get_data().decode(encoding="utf-8")
    print(f"Received text: {text}")
    return text


@domain.route("/text/sentences", methods=["POST"])
def segment_text():
    text = request.get_data().decode(encoding="utf-8")
    print(f"Received: {text[:100]}")
    sents = domain_controller.from_raw_to_sentenced(text)
    print(f"Found {len[text]} sentences")
    return sents


@domain.route("/text/tokenize", methods=["POST"])
def tokenize_text():
    text = request.get_data().decode(encoding="utf-8")
    print(f"Received: {text[:100]}")
    tokenized = domain_controller.from_raw_to_tokenized_sentences(text)
    print(f"Tokenized {len(tokenized)} sentences")
    return tokenized


@domain.route("/text/tag", methods=["POST"])
def tag_text():
    text = request.get_data().decode(encoding="utf-8")
    print(f"Received: {text[:100]}")
    tagged_sents = domain_controller.from_raw_to_tagged_sentences(text)
    print(f"Tagged {len(tagged_sents)} sentences")
    return tagged_sents


@domain.route("/text/tag/universal", methods=["POST"])
def univeral_tag_text():
    text = request.get_data().decode(encoding="utf-8")
    print(f"Received: {text[:100]}")
    universal_tagged_sents = domain_controller.from_raw_to_universal_tagged_sentences(
        text
    )
    print(f"Tagged universally {len(universal_tagged_sents)} sentences")
    return universal_tagged_sents


@domain.route("/text/lemmas", methods=["POST"])
def text_lemmas():
    text = request.get_data().decode(encoding="utf-8")
    print(f"Received: {text[:100]}")
    lemmas_to_universal_poses = domain_controller.from_raw_to_lemmas(text)
    normalized_response = {
        lemma: list(uposes) for lemma, uposes in lemmas_to_universal_poses.items()
    }
    return normalized_response


@domain.route("/text/definitions", methods=["POST"])
def text_definitions():
    text = request.get_data().decode(encoding="utf-8")
    print(f"Received: {text[:100]}")
    definitions = domain_controller.from_raw_to_definitions(text)
    print(f"Found definitions for {len(definitions)} words")
    return __definitions_to_json(definitions)


@domain.route("/text/definitions/<title>")
def text_definitions_by_text_title(title: str):
    definitions = domain_controller.from_title_to_definitions(title)
    print(f"Found definitions: {len(definitions)}")
    json = __definitions_to_json(definitions)
    print(f"Sending: {json}")
    return json
