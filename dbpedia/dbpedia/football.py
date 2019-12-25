from refo import Plus, Question
from quepy.dsl import HasKeyword
from quepy.parsing import Lemma, Lemmas, Pos, QuestionTemplate, Particle, Token
from dsl import NameOf, IsPerson, IsPlace, IsFootballTeam, ManagerOf, LabelOf, IsStadium, StadiumOf, CapacityOfStadium, CapacityOfTeam, LabelOf, TrophiesOf
from synonyms import Synonyms

synonyms_ref = Synonyms() 

nouns = Plus(Pos("FW") | Pos("NN") | Pos("NNP") | Pos("NNS") | Pos("NNPS"))

class Team(Particle):
    regex = nouns

    def interpret(self, match):
        name = match.words.tokens
        return IsFootballTeam() + HasKeyword(name)


class Stadium(Particle):
    regex = nouns

    def interpret(self, match):
        name = match.words.tokens
        return IsStadium() + HasKeyword(name)


class WhoIsCoachOfQuestion(QuestionTemplate):
    """
    Ex: "Coach of team FC Barcelona"
        "who is the coach of team CFR Cluj?"
    """
    coach_wordnet = synonyms_ref.getLemmaPreposition("coach", 'n')
    regex = Question(Lemmas("who be")) + Question(Pos("DT")) + coach_wordnet + Question(Pos("IN")) + Question(Pos("DT")) + Token("team") + Team() + Question(Pos("."))

    def interpret(self, match):
        coach = ManagerOf(match.team)
        return LabelOf(coach), "enum"


class WhatIsTheStadiumOfQuestion(QuestionTemplate):
    """
    Ex: "What is the stadium of FC Barcelona?"
        "Arena of FC Steaua Bucuresti"
    """

    stadium_wordnet = synonyms_ref.getLemmaPreposition("stadium", 'n')
    regex = Question(Pos("WP") + Lemma("be")) + Question(Pos("DT")) + stadium_wordnet + Question(Pos("IN")) + Team() + Question(Pos("."))

    def interpret(self, match):
        stadium = StadiumOf(match.team)
        return LabelOf(stadium), "enum"


class TeamWhatIsTheCapacityOfQuestion(QuestionTemplate):
    """
    Ex: "What is the capacity of the stadium of FC Barcelona?"
        "Capacity of the stadium of FC Barcelona"
    """

    stadium_wordnet = synonyms_ref.getLemmaPreposition("stadium", 'n')
    opening = Question(Pos("WP") + Lemma("be")) + Question(Pos("DT")) + Lemma("capacity")
    regex = opening + Question(Pos("IN")) + Question(Pos("DT")) + stadium_wordnet + Question(Pos("IN")) + Team() + Question(Pos("."))
    
    def interpret(self, match):
        capacity = CapacityOfTeam(match.team)
        return capacity, "literal"


class StadiumWhatIsTheCapacityOfQuestion(QuestionTemplate):
    """
    Ex: "What is the capacity of Camp Nou?"
        "Capacity of Old Trafford"
    """

    stadium_wordnet = synonyms_ref.getLemmaPreposition("stadium", 'n')
    opening = Question(Pos("WP") + Lemma("be")) + Question(Pos("DT")) + Lemma("capacity")
    regex = opening + Question(Pos("IN")) + Stadium() + Question(Pos("."))

    def interpret(self, match):
        capacity = CapacityOfStadium(match.stadium)
        return capacity, "literal"


class TrophiesQuestion(QuestionTemplate):
    """
    Ex: "List CFR Cluj throphies"
        "FC Barcelona awards"
        "Enumerate FC Barcelona accolades"
    """

    list_wordnet = synonyms_ref.getLemmaPreposition("list", 'v')
    trophy_wordnet = synonyms_ref.getLemmaPreposition("trophy", 'n')
    regex = Question(list_wordnet) + Team() + trophy_wordnet + Question(Pos("."))

    def interpret(self, match):
        trophies = TrophiesOf(match.team)
        return LabelOf(trophies), "enum"