# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
People related regex
"""

from refo import Plus, Question
from quepy.dsl import HasKeyword
from quepy.parsing import Lemma, Lemmas, Pos, QuestionTemplate, Particle
from dsl import IsPerson, LabelOf, DefinitionOf, BirthDateOf, BirthPlaceOf, HasParents, HasChildren, HasSpouse, ResidenceOf


class Person(Particle):
    regex = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

    def interpret(self, match):
        name = match.words.tokens
        return IsPerson() + HasKeyword(name)


class WhoIs(QuestionTemplate):
    """
    Ex: "Who is Tom Cruise?"
    """

    regex = Lemma("who") + Lemma("be") + Person() + \
        Question(Pos("."))

    def interpret(self, match):
        definition = DefinitionOf(match.person)
        return definition, "define"


class HowOldIsQuestion(QuestionTemplate):
    """
    Ex: "How old is Bob Dylan".
    """

    regex = Pos("WRB") + Lemma("old") + Lemma("be") + Person() + \
        Question(Pos("."))

    def interpret(self, match):
        birth_date = BirthDateOf(match.person)
        return birth_date, "age"


class WhereIsFromQuestion(QuestionTemplate):
    """
    Ex: "Where is Bill Gates from?"
    """

    regex = Lemmas("where be") + Person() + Lemma("from") + \
        Question(Pos("."))

    def interpret(self, match):
        birth_place = BirthPlaceOf(match.person)
        label = LabelOf(birth_place)

        return label, "enum"


class WhoAreTheParentsOfQuestion(QuestionTemplate):
    """
    Ex: "Who are the parents of Bill Gates?"
    """

    regex = Lemmas("who be") + Question(Pos("DT")) + Lemma("parent") + Question(Pos("IN")) + Person() + Question(Pos("."))

    def interpret(self, match):
        name = HasParents(match.person)

        return LabelOf(name), "enum"


class WhoAreTheChildrenOfQuestion(QuestionTemplate):
    """
    Ex: "Who are the children of Donald Trump?"
    """

    regex = Lemmas("who be") + Question(Pos("DT")) + Lemma("child") + Question(Pos("IN")) + Person() + Question(Pos("."))

    def interpret(self, match):
        name = HasChildren(match.person)

        return LabelOf(name), "enum"


class WhoIsTheSpouseOfQuestion(QuestionTemplate):
    """
    Ex: "Who is the spouse of Barack Obama?"
    """

    regex = Lemmas("who be") + Question(Pos("DT")) + Lemma("spouse") + Question(Pos("IN")) + Person() + Question(Pos("."))

    def interpret(self, match):
        name = HasSpouse(match.person)

        return LabelOf(name), "enum"


class WhereLivesQuestion(QuestionTemplate):
    """
    Ex: "Where does Donald Trump live?"
    """

    regex = Lemma("where") + Question(Lemma("do")) + Person() + Lemma("live") + Question(Pos("."))

    def interpret(self, match):
        residence = ResidenceOf(match.person)

        return LabelOf(residence), "enum"