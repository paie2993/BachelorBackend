import nltk

from flask import make_response
from flask import Blueprint
from flask import request
from application.ioc_container.container import container
from application.web.controllers.control_controller import ControlController


control_controller: ControlController = container.resolve(ControlController)

control = Blueprint("control", __name__)


@control.route("/texts/names")
def text_names():
    return nltk.corpus.gutenberg.fileids()


@control.route("/texts/content/<name>")
def text_content(name: str):
    if name not in nltk.corpus.gutenberg.fileids():
        return f"No such text: {name}"
    return nltk.corpus.gutenberg.raw(name)


@control.route(
    "/dictionary/seed/specific/<name>",
)
def seed_specific_by_name(name: str):
    if name not in nltk.corpus.gutenberg.fileids():
        return f"No such text: {name}"
    control_controller.seed_dictionary_with_text_by_name(name)
    return make_response()


@control.route("/dictionary/seed/specific", methods=["POST"])
def seed_specific_by_text():
    text = request.get_data().decode("utf-8")
    control_controller.seed_dictionary_with_raw_text(text)
    return make_response()


@control.route("/dictionary/seed/random/<count>")
def seed_random(count: int):
    control_controller.seed_dictionary_with_random_words(count)
    return make_response()
