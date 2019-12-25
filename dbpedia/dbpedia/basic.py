# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Basic questions for DBpedia.
"""

from refo import Group, Plus, Question
from quepy.parsing import Lemma, Pos, QuestionTemplate, Token, Particle, Lemmas
from quepy.dsl import HasKeyword, IsRelatedTo, HasType
from dsl import DefinitionOf, LabelOf, IsPlace, UTCof, LocationOf
from synonyms import Synonyms

synonyms_ref = Synonyms() 

class Thing(Particle):
    regex = Question(Pos("JJ")) + (Pos("NN") | Pos("NNP") | Pos("NNS")) | Pos("VBN")

    def interpret(self, match):
        return HasKeyword(match.words.tokens)


class WhatIs(QuestionTemplate):
    """
    Regex for questions like "What is a blowtorch
    Ex: "What is a car"
        "What is Seinfield?"
    """

    regex = Lemma("what") + Lemma("be") + Question(Pos("DT")) + Thing() + Question(Pos("."))

    def interpret(self, match):

        label = DefinitionOf(match.thing)

        return label, "define"


class ListEntity(QuestionTemplate):
    """
    Regex for questions like "List Microsoft software"
    """
    
    entity = Group(Pos("NNP"), "entity")
    target = Group(Pos("NN") | Pos("NNS"), "target")
    list_wordnet = synonyms_ref.getLemmaPreposition("list", 'v')
    regex =  list_wordnet + entity + target

    def interpret(self, match):
        entity = HasKeyword(match.entity.tokens)
        target_type = HasKeyword(match.target.lemmas)
        target = HasType(target_type) + IsRelatedTo(entity)
        label = LabelOf(target)

        return label, "enum"


class WhatTimeIs(QuestionTemplate):
    """
    Regex for questions about the time
    Ex: "What time is it in Cordoba"
    """

    nouns = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))
    place = Group(nouns, "place")
    time_wordnet = synonyms_ref.getLemmaPreposition("time", 'n')
    openings = (Lemma("what") +
        ((Token("is") + Token("the") + Question(Lemma("current")) +
        Question(Lemma("local")) + time_wordnet) |
        (time_wordnet + Token("is") + Token("it")))) | time_wordnet
    regex = openings + Pos("IN") + place + Question(Pos("."))

    def interpret(self, match):
        place = HasKeyword(match.place.lemmas.title()) + IsPlace()
        utc_offset = UTCof(place)

        return utc_offset, "time"


class WhereIsQuestion(QuestionTemplate):
    """
    Ex: "where in the world is the Eiffel Tower"
    """

    thing = Group(Plus(Pos("IN") | Pos("NP") | Pos("NNP") | Pos("NNPS")), "thing")
    world_wordnet = synonyms_ref.getLemmaPreposition("world", 'n')
    regex = Lemma("where") + Question(Pos("IN")) + Question(Pos("DT")) + Question(world_wordnet) + Lemma("be") + \
        Question(Pos("DT")) + thing + Question(Pos("."))

    def interpret(self, match):
        thing = HasKeyword(match.thing.tokens)
        location = LocationOf(thing)
        location_name = LabelOf(location)

        return location_name, "enum"

