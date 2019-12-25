# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Country related regex
"""

from refo import Plus, Question
from quepy.dsl import HasKeyword
from quepy.parsing import Lemma, Pos, QuestionTemplate, Token, Particle
from dsl import IsCountry, IncumbentOf, CapitalOf, LabelOf, LanguageOf, PopulationOf, PresidentOf, CurrencyOf, GovernmentTypeOf
from synonyms import Synonyms

synonyms_ref = Synonyms() 


class Country(Particle):
    regex = Plus(Pos("DT") | Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

    def interpret(self, match):
        name = match.words.tokens.title()
        return IsCountry() + HasKeyword(name)


class PresidentOfQuestion(QuestionTemplate):
    """
    Regex for questions about the president of a country.
    Ex: "Who is the president of Argentina?"
    """

    wordnet_president = synonyms_ref.getLemmaPreposition("president", 'n')
    regex = Pos("WP") + Token("is") + Question(Pos("DT")) + wordnet_president + Pos("IN") + Country() + Question(Pos("."))

    def interpret(self, match):
        president = PresidentOf(match.country)
        # incumbent = IncumbentOf(president)
        label = LabelOf(president)
        return label, "enum"


class CapitalOfQuestion(QuestionTemplate):
    """
    Regex for questions about the capital of a country.
    Ex: "What is the capital of Bolivia?"
    """

    opening = Lemma("what") + Token("is")
    regex = opening + Pos("DT") + Lemma("capital") + Pos("IN") + \
        Question(Pos("DT")) + Country() + Question(Pos("."))

    def interpret(self, match):
        capital = CapitalOf(match.country)
        label = LabelOf(capital)
        return label, "enum"


class LanguageOfQuestion(QuestionTemplate):
    """
    Regex for questions about the language spoken in a country.
    Ex: "What is the language of Argentina?"
        "what language is spoken in Argentina?"
    """

    openings = (Lemma("what") + Token("is") + Pos("DT") +
                Question(Lemma("official")) + Lemma("language")) | \
               (Lemma("what") + Lemma("language") + Token("is") +
                Lemma("speak"))

    regex = openings + Pos("IN") + Question(Pos("DT")) + Country() + \
        Question(Pos("."))

    def interpret(self, match):
        language = LabelOf(LanguageOf(match.country))
        return language, "enum"


class PopulationOfQuestion(QuestionTemplate):
    """
    Regex for questions about the population of a country.
    Ex: "What is the population of China?"
        "How many people live in China?"
    """

    people_wordnet = synonyms_ref.getLemmaPreposition("people", 'n')
    live_wordnet = synonyms_ref.getLemmaPreposition("live", 'v')
    openings = (Pos("WP") + Token("is") + Pos("DT") +
                Lemma("population") + Pos("IN")) | \
               (Pos("WRB") + Lemma("many") + people_wordnet +
                live_wordnet + Pos("IN"))
    regex = openings + Question(Pos("DT")) + Country() + Question(Pos("."))

    def interpret(self, match):
        population = PopulationOf(match.country)
        return population, "literal"


class CurrencyOfQuestion(QuestionTemplate): 
    """
    Regex for questions about the currency of a country.
    Ex: "What is the currency of China?"
        "Money of Japan"
    """

    currency_wordnet = synonyms_ref.getLemmaPreposition("currency", 'n') | synonyms_ref.getLemmaPreposition("money", 'n')
    regex = Question(Pos("WP") + Token("is") + Question(Pos("DT"))) + currency_wordnet + Pos("IN") + Country() + Question(Pos("."))

    def interpret(self, match):
        currency = CurrencyOf(match.country)
        return LabelOf(currency), "enum"


class GovernmentTypeOfQuestion(QuestionTemplate):
    """
    Regex for questions about the government type of a country.
    Ex: "What is the government type of Romania?"
        "Form of government in Romania"
    """

    government_wordnet = synonyms_ref.getLemmaPreposition("government", 'n')
    type_wordnet = synonyms_ref.getLemmaPreposition("type", 'n')
    opening = Question(Pos("WP") + Token("is") + Question(Pos("DT")))
    regex = (opening + government_wordnet + Question(type_wordnet) + Pos("IN") + Country() + Question(Pos("."))) | \
            (opening + Question(type_wordnet) + Pos("IN") + government_wordnet + Pos("IN") + Country() + Question(Pos(".")))
    
    def interpret(self, match):
        form = GovernmentTypeOf(match.country)
        return LabelOf(form), "enum"