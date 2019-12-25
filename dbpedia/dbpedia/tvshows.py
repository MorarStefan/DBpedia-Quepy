# coding: utf-8

"""
Tv Shows related regex.
"""

from refo import Plus, Question
from quepy.dsl import HasKeyword
from quepy.parsing import Lemma, Lemmas, Pos, QuestionTemplate, Particle, Token
from dsl import IsTvShow, ReleaseDateOf, IsPerson, StarsIn, LabelOf, \
    HasShowName, NumberOfEpisodesIn, HasActor, ShowNameOf, CreatorOf
from synonyms import Synonyms

synonyms_ref = Synonyms() 

nouns = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))


class TvShow(Particle):
    regex = Plus(Question(Pos("DT")) + nouns)

    def interpret(self, match):
        name = match.words.tokens
        return IsTvShow() + HasShowName(name)


class Actor(Particle):
    regex = nouns

    def interpret(self, match):
        name = match.words.tokens
        return IsPerson() + HasKeyword(name)


class ReleaseDateQuestion(QuestionTemplate):
    """
    Ex: when was Friends released?
    """

    release_wordnet = synonyms_ref.getLemmaPreposition("release", 'v')
    regex = Lemmas("when be") + TvShow() + release_wordnet + Question(Pos("."))

    def interpret(self, match):
        release_date = ReleaseDateOf(match.tvshow)
        return release_date, "literal"


class CastOfQuestion(QuestionTemplate):
    """
    Ex: "What is the cast of Friends?"
        "Who works in Breaking Bad?"
        "List actors of Seinfeld"
    """

    regex = (Question(Lemmas("what be") + Pos("DT")) +
             Lemma("cast") + Pos("IN") + TvShow() + Question(Pos("."))) | \
            (Lemmas("who works") + Pos("IN") + TvShow() +
             Question(Pos("."))) | \
            (Lemmas("list actor") + Pos("IN") + TvShow())

    def interpret(self, match):
        actor = IsPerson() + StarsIn(match.tvshow)
        name = LabelOf(actor)
        return name, "enum"


class ListTvShows(QuestionTemplate):
    """
    Ex: "List TV shows"
    """

    list_wordnet = synonyms_ref.getLemmaPreposition("list", 'v')
    regex = list_wordnet + Lemmas("tv show")

    def interpret(self, match):
        show = IsTvShow()
        label = LabelOf(show)
        return label, "enum"


class EpisodeCountQuestion(QuestionTemplate):
    """
    Ex: "How many episodes does Seinfeld have?"
        "Number of episodes of Seinfeld"
    """

    regex = ((Lemmas("how many episode do") + TvShow() + Lemma("have")) |
             (Lemma("number") + Pos("IN") + Lemma("episode") +
              Pos("IN") + TvShow())) + \
            Question(Pos("."))

    def interpret(self, match):
        number_of_episodes = NumberOfEpisodesIn(match.tvshow)
        return number_of_episodes, "literal"


class ShowsWithQuestion(QuestionTemplate):
    """
    Ex: "List shows with Hugh Laurie"
        "In what shows does Jennifer Aniston appears?"
        "Shows with Matt LeBlanc"
    """

    regex = (Lemmas("list show") + Pos("IN") + Actor()) | \
            (Pos("IN") + (Lemma("what") | Lemma("which")) + Lemmas("show do") +
             Actor() + (Lemma("appear") | Lemma("work")) +
             Question(Pos("."))) | \
            ((Lemma("show") | Lemma("shows")) + Pos("IN") + Actor())

    def interpret(self, match):
        show = IsTvShow() + HasActor(match.actor)
        show_name = ShowNameOf(show)
        return show_name, "enum"


class CreatorOfQuestion(QuestionTemplate):
    """
    Ex: "Who is the creator of Breaking Bad?"
    """

    regex = Question(Lemmas("who be") + Pos("DT")) + \
        Lemma("creator") + Pos("IN") + TvShow() + Question(Pos("."))

    def interpret(self, match):
        creator = CreatorOf(match.tvshow)
        label = LabelOf(creator)
        return label, "enum"
