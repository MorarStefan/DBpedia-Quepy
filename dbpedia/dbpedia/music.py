# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Music related regex
"""

from refo import Plus, Question
from quepy.dsl import HasKeyword
from quepy.parsing import Lemma, Lemmas, Pos, QuestionTemplate, Particle
from dsl import IsBand, LabelOf, IsMemberOf, ActiveYears, MusicGenreOf, \
    NameOf, IsAlbum, ProducedBy, AssociatedActsOf
from synonyms import Synonyms

synonyms_ref = Synonyms() 

class Band(Particle):
    regex = Question(Pos("DT")) + Plus(Pos("NN") | Pos("NNP"))

    def interpret(self, match):
        name = match.words.tokens.title()
        return IsBand() + HasKeyword(name)


class BandMembersQuestion(QuestionTemplate):
    """
    Regex for questions about band member.
    Ex: "Radiohead members"
        "What are the members of Metallica?"
    """

    regex1 = Band() + Lemma("member")
    regex2 = Lemma("member") + Pos("IN") + Band()
    regex3 = Pos("WP") + Lemma("be") + Pos("DT") + Lemma("member") + \
        Pos("IN") + Band()

    regex = (regex1 | regex2 | regex3) + Question(Pos("."))

    def interpret(self, match):
        member = IsMemberOf(match.band)
        label = LabelOf(member)
        return label, "enum"


class FoundationQuestion(QuestionTemplate):
    """
    Regex for questions about the creation of a band.
    Ex: "When was Pink Floyd founded?"
        "When was Korn formed?"
    """

    founded_wordnet = synonyms_ref.getLemmaPreposition("founded", 'v') | synonyms_ref.getLemmaPreposition("formed", 'v')
    regex = Pos("WRB") + Lemma("be") + Band() + founded_wordnet + Question(Pos("."))

    def interpret(self, match):
        active_years = ActiveYears(match.band)
        return active_years, "literal"


class GenreQuestion(QuestionTemplate):
    """
    Regex for questions about the genre of a band.
    Ex: "What is the music genre of Gorillaz?"
        "Music genre of Radiohead"
    """

    genre_wordnet = synonyms_ref.getLemmaPreposition("genre", 'n')
    optional_opening = Question(Pos("WP") + Lemma("be") + Pos("DT"))
    regex = optional_opening + genre_wordnet + \
        Pos("IN") + Band() + Question(Pos("."))

    def interpret(self, match):
        genre = MusicGenreOf(match.band)
        label = LabelOf(genre)
        return label, "enum"


class AlbumsOfQuestion(QuestionTemplate):
    """
    Ex: "List albums of Pink Floyd"
        "What albums did Pearl Jam record?"
        "Albums by Metallica"
    """

    regex = (Question(Lemma("list")) + (Lemma("album") | Lemma("albums")) + \
             Pos("IN") + Band()) | \
            (Lemmas("what album do") + Band() +
             (Lemma("record") | Lemma("make")) + Question(Pos("."))) | \
            (Lemma("list") + Band() + Lemma("album"))

    def interpret(self, match):
        album = IsAlbum() + ProducedBy(match.band)
        name = NameOf(album)
        return name, "enum"


class RecommendBandsQuestion(QuestionTemplate):
    """
    Ex: "Recommend bands like Metallica"
        "Suggest bands like Led Zeppelin"
    """

    recommend_wordnet = synonyms_ref.getLemmaPreposition("recommend", 'v')
    band_wordnet = synonyms_ref.getLemmaPreposition("band", 'n')
    regex = recommend_wordnet + Question(band_wordnet) + Question(Lemma("like")) + Band()

    def interpret(self, match):
        names = AssociatedActsOf(match.band)
        return LabelOf(names), "enum"

