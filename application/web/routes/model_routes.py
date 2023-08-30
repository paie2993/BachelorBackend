from flask import Blueprint, make_response
from ml_models.models import ModelFiles
from ml_models.trainer import Trainer
from resources.preconditions.environment.environment import (
    HYPHENED_WORD_CLASSIFIER_FILENAME,
    POS_TAGGER_FILENAME,
)

from application.ioc_container.container import container
from text_processing.hyphened.classifier import Classifier
from text_processing.hyphened.extractor import HyphenedFeatureExtractor
from text_processing.tagging.pos_tagging.pos_tagger import Tagger


def train_models():
    trainer: Trainer = container.resolve(Trainer)
    tagger = container.resolve(Tagger)
    feature_extractor = container.resolve(HyphenedFeatureExtractor)
    classifier = container.resolve(Classifier)
    trainer.train_models(tagger, feature_extractor, classifier)


def cleanup_models():
    model_files: ModelFiles = container.resolve(ModelFiles)
    model_files.clean(POS_TAGGER_FILENAME)
    model_files.clean(HYPHENED_WORD_CLASSIFIER_FILENAME)


model = Blueprint("model", __name__)


@model.route("/models/train")
def train():
    train_models()
    return make_response()


@model.route("/models/cleanup")
def cleanup():
    cleanup_models()
    return make_response()
