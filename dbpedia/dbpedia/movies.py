# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Movie related regex.
"""

from refo import Plus, Question
from quepy.dsl import HasKeyword
from quepy.parsing import Lemma, Lemmas, Pos, QuestionTemplate, Particle
from dsl import IsMovie, NameOf, IsPerson, \
    DirectedBy, LabelOf, DurationOf, HasActor, HasName, ReleaseDateOf, \
    DirectorOf, StarsIn, DefinitionOf
from synonyms import Synonyms

synonyms_ref = Synonyms() 

nouns = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))


class Movie(Particle):
    regex = Question(Pos("DT")) + nouns

    def interpret(self, match):
        name = match.words.tokens
        return IsMovie() + HasName(name)


class Actor(Particle):
    regex = nouns

    def interpret(self, match):
        name = match.words.tokens
        return IsPerson() + HasKeyword(name)


class CoStar(Particle):
    regex = nouns

    def interpret(self, match):
        name = match.words.tokens
        return IsPerson() + HasKeyword(name)

class Director(Particle):
    regex = nouns

    def interpret(self, match):
        name = match.words.tokens
        return IsPerson() + HasKeyword(name)


class ListMoviesQuestion(QuestionTemplate):
    """
    Ex: "list movies"
    """

    list_wordnet = synonyms_ref.getLemmaPreposition("list", 'v')
    film_wordnet = synonyms_ref.getLemmaPreposition("film", 'n')

    regex = list_wordnet + film_wordnet

    def interpret(self, match):
        movie = IsMovie()
        name = NameOf(movie)
        return name, "enum"


class MoviesByDirectorQuestion(QuestionTemplate):
    """
    Ex: "List movies directed by Quentin Tarantino.
        "movies directed by Martin Scorsese"            
        "which movies did Mel Gibson directed"
    """

    list_wordnet = synonyms_ref.getLemmaPreposition("list", 'v')
    film_wordnet = synonyms_ref.getLemmaPreposition("film", 'n')
    direct_wordnet = synonyms_ref.getLemmaPreposition("direct", 'v')

    regex = (Question(list_wordnet) + film_wordnet +   
             Question(direct_wordnet) + Lemma("by") + Director()) | \
             (Lemma("which") + film_wordnet + Lemma("do") +
             Director() + direct_wordnet + Question(Pos("."))) 

    def interpret(self, match):
        movie = IsMovie() + DirectedBy(match.director)
        movie_name = LabelOf(movie)

        return movie_name, "enum"


class MovieDurationQuestion(QuestionTemplate):
    """
    Ex: "How long is Pulp Fiction"
        "What is the duration of The Thin Red Line?"
    """

    duration_wordnet = synonyms_ref.getLemmaPreposition("duration", 'n')
    
    regex = ((Lemmas("how long be") + Movie()) |
            (Lemmas("what be") + Pos("DT") + duration_wordnet +
             Pos("IN") + Movie())) + \
            Question(Pos("."))

    def interpret(self, match):
        duration = DurationOf(match.movie)
        return duration, ("literal", "{} minutes long")


class ActedOnQuestion(QuestionTemplate):
    """
    Ex: "List movies with Hugh Laurie"
        "Movies with Matt LeBlanc"
        "In what movies did Jennifer Aniston appear?"
        "Which movies did Mel Gibson starred?"
        "Movies starring Winona Ryder"
    """
    
    acted_on_wordnet = synonyms_ref.getLemmaPreposition("star", 'v') | synonyms_ref.getLemmaPreposition("appear", 'v') | synonyms_ref.getLemmaPreposition("act", 'v')
    film_wordnet = synonyms_ref.getLemmaPreposition("film", 'n')

    regex = (Question(Lemma("list")) + film_wordnet + Lemma("with") + Actor()) | \
            (Question(Pos("IN")) + (Lemma("what") | Lemma("which")) +
             film_wordnet + Lemma("do") + Actor() + acted_on_wordnet + Question(Pos("."))) | \
            (Question(Pos("IN")) + Lemma("which") + film_wordnet + Lemma("do") +
            Actor() + acted_on_wordnet) | \
            (Question(Lemma("list")) + film_wordnet + Lemma("star") + Actor())

    def interpret(self, match):
        movie = IsMovie() + HasActor(match.actor)
        movie_name = NameOf(movie)
        return movie_name, "enum"


class ActedOnTwoQuestion(QuestionTemplate):
    """
    Ex: "List movies with Hugh Laurie and James Woods"
        "Movies with Matt LeBlanc and Chevy Chase"
        "In what movies did Jennifer Aniston and Stephen Root appear?"
        "Which movies did Kate Winslet and Leonardo DiCaprio starred?"
        "Movies starring Winona Ryder and Cher"
    """
    
    acted_on_wordnet = synonyms_ref.getLemmaPreposition("star", 'v') | synonyms_ref.getLemmaPreposition("appear", 'v') | synonyms_ref.getLemmaPreposition("act", 'v')
    film_wordnet = synonyms_ref.getLemmaPreposition("film", 'n')
    actors = Actor() + Pos("CC") + CoStar()

    regex = (Question(Lemma("list")) + film_wordnet + Lemma("with") + actors) | \
            (Question(Pos("IN")) + (Lemma("what") | Lemma("which")) +
             film_wordnet + Lemma("do") + actors + acted_on_wordnet + Question(Pos("."))) | \
            (Question(Pos("IN")) + Lemma("which") + film_wordnet + Lemma("do") +
            actors + acted_on_wordnet) | \
            (Question(Lemma("list")) + film_wordnet + Lemma("star") + actors)

    def interpret(self, match):
        movie = IsMovie() + HasActor(match.actor) + HasActor(match.costar)
        movie_name = NameOf(movie)
        return movie_name, "enum"


class MovieReleaseDateQuestion(QuestionTemplate):
    """
    Ex: "When was The Red Thin Line released?"
        "Release date of The Empire Strikes Back"
    """

    release_wordnet = synonyms_ref.getLemmaPreposition("release", 'v')

    regex = ((Lemmas("when be") + Movie() + release_wordnet) |
            (release_wordnet + Question(Lemma("date")) +
             Pos("IN") + Movie())) + \
            Question(Pos("."))

    def interpret(self, match):
        release_date = ReleaseDateOf(match.movie)
        return release_date, "literal"


class DirectorOfQuestion(QuestionTemplate):
    """
    Ex: "Who is the director of Big Fish?"
        "who directed Pocahontas?"
    """

    director_wordnet = synonyms_ref.getLemmaPreposition("director", 'n')
    direct_wordnet = synonyms_ref.getLemmaPreposition("direct", 'v')

    regex = ((Lemmas("who be") + Pos("DT") + director_wordnet +
             Pos("IN") + Movie()) |
             (Lemma("who") + direct_wordnet + Movie())) + \
            Question(Pos("."))

    def interpret(self, match):
        director = IsPerson() + DirectorOf(match.movie)
        director_name = NameOf(director)
        return director_name, "literal"


class ActorsOfQuestion(QuestionTemplate):
    """
    Ex: "who are the actors of Titanic?"
        "who acted in Alien?"
        "who starred in Depredator?"
        "Actors of Fight Club"
    """

    acted_on_wordnet = synonyms_ref.getLemmaPreposition("star", 'v') | synonyms_ref.getLemmaPreposition("appear", 'v') | synonyms_ref.getLemmaPreposition("act", 'v')

    regex = (Lemma("who") + Question(Lemma("be") + Pos("DT")) +
             (acted_on_wordnet | Lemma("actor")) +
             Pos("IN") + Movie() + Question(Pos("."))) | \
            ((Lemma("actors") | Lemma("actor")) + Pos("IN") + Movie())

    def interpret(self, match):
        actor = NameOf(IsPerson() + StarsIn(match.movie))
        return actor, "enum"


class PlotOfQuestion(QuestionTemplate):
    """
    Ex: "what is Shame about?"
        "plot of Titanic"
    """

    plot_wordnet = synonyms_ref.getLemmaPreposition("plot", 'n')

    regex = ((Lemmas("what be") + Movie() + Lemma("about")) | \
             (Question(Lemmas("what be the")) + plot_wordnet +
              Pos("IN") + Movie())) + \
            Question(Pos("."))

    def interpret(self, match):
        definition = DefinitionOf(match.movie)
        return definition, "define"

