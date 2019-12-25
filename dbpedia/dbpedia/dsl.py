# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Domain specific language for DBpedia quepy.
"""

from quepy.dsl import FixedType, HasKeyword, FixedRelation, FixedDataRelation

# Setup the Keywords for this application
HasKeyword.relation = "rdfs:label"
HasKeyword.language = "en"


class IsPerson(FixedType):
    fixedtype = "foaf:Person"

class IsPlace(FixedType):
    # fixedtype = "dbpedia:Place"
    fixedtype = "dbo:Place"


class IsCountry(FixedType):
    # fixedtype = "dbpedia-owl:Country"
    fixedtype = "dbo:Country"


class IsPopulatedPlace(FixedType):
    # fixedtype = "dbpedia-owl:PopulatedPlace"
    fixedtype = "dbo:PopulatedPlace"


class IsBand(FixedType):
    # fixedtype = "dbpedia-owl:Band"
    fixedtype = "dbo:Band"


class IsAlbum(FixedType):
    # fixedtype = "dbpedia-owl:Album"
    fixedtype = "dbo:Album"


class IsTvShow(FixedType):
    # fixedtype = "dbpedia-owl:TelevisionShow"
    fixedtype = "dbo:TelevisionShow" 


class IsMovie(FixedType):
    # fixedtype = "dbpedia-owl:Film" 
    fixedtype = "dbo:Film"  


class HasShowName(FixedDataRelation):
    # relation = "dbpprop:showName"
    relation = "foaf:name"
    language = "en"


class HasName(FixedDataRelation):
    # relation = "dbpprop:name"
    relation = "foaf:name" 
    language = "en"


class DefinitionOf(FixedRelation):
    relation = "rdfs:comment"
    reverse = True


class LabelOf(FixedRelation):
    relation = "rdfs:label"
    reverse = True


class UTCof(FixedRelation):
    relation = "dbpprop:utcOffset"
    reverse = True


class PresidentOf(FixedRelation):
    # relation = "dbpprop:leaderTitle"
    relation = "dbo:leader"
    reverse = True


class IncumbentOf(FixedRelation):
    # relation = "dbpprop:incumbent"
    relation = "dbp:incumbent"
    #reverse = True


class CapitalOf(FixedRelation):
    # relation = "dbpedia-owl:capital"
    relation = "dbo:capital" 
    reverse = True


class LanguageOf(FixedRelation):
    # relation = "dbpprop:officialLanguages"
    relation = "dbo:language"
    reverse = True


class PopulationOf(FixedRelation):
    # relation = "dbpprop:populationCensus"
    relation = "dbo:populationTotal" 
    reverse = True


class IsMemberOf(FixedRelation):
    # relation = "dbpedia-owl:bandMember"
    relation = "dbo:bandMember"
    reverse = True


class ActiveYears(FixedRelation):
    # relation = "dbpprop:yearsActive"
    relation = "dbo:activeYearsStartYear" 
    reverse = True


class MusicGenreOf(FixedRelation):
    # relation = "dbpedia-owl:genre"
    relation = "dbo:genre"
    reverse = True


class ProducedBy(FixedRelation):
    # relation = "dbpedia-owl:producer"
    relation = "dbo:producer"


class BirthDateOf(FixedRelation):
    relation = "dbpprop:birthDate"
    reverse = True


class BirthPlaceOf(FixedRelation):
    # relation = "dbpedia-owl:birthPlace"
    relation = "dbo:birthPlace"
    reverse = True


class ReleaseDateOf(FixedRelation):
    # relation = "dbpedia-owl:releaseDate"
    relation = "dbo:releaseDate"
    reverse = True


class StarsIn(FixedRelation):
    # relation = "dbpprop:starring"
    relation = "dbo:starring" 
    reverse = True


class NumberOfEpisodesIn(FixedRelation):
    # relation = "dbpedia-owl:numberOfEpisodes"
    relation = "dbo:numberOfEpisodes" 
    reverse = True


class ShowNameOf(FixedRelation):
     # relation = "dbpprop:showName"
    relation = "foaf:name"
    reverse = True


class HasActor(FixedRelation):
    # relation = "dbpprop:starring"
    relation = "dbo:starring" 


class CreatorOf(FixedRelation):
    # relation = "dbpprop:creator"
    relation = "dbo:creator" 
    reverse = True


class NameOf(FixedRelation):
    # relation = "dbpprop:name"
    relation = "foaf:name" 
    reverse = True


class DirectedBy(FixedRelation):
    # relation = "dbpedia-owl:director"
    relation = "dbo:director"


class DirectorOf(FixedRelation):
    # relation = "dbpedia-owl:director"
    relation = "dbo:director"
    reverse = True


class DurationOf(FixedRelation):
    # DBpedia throws an error if the relation it's
    # dbpedia-owl:Work/runtime so we expand the prefix
    # by giving the whole URL.
    relation = "<http://dbpedia.org/ontology/Work/runtime>"
    reverse = True


class HasAuthor(FixedRelation):
    # relation = "dbpedia-owl:author"
    relation = "dbo:author"


class AuthorOf(FixedRelation):
    # relation = "dbpedia-owl:author"
    relation = "dbo:author"
    reverse = True


class IsBook(FixedType):
    # fixedtype = "dbpedia-owl:Book"
    fixedtype = "dbo:Book"


class LocationOf(FixedRelation):
    # relation = "dbpedia-owl:location"
    relation = "dbo:location"
    reverse = True

###########################################

class ManagerOf(FixedRelation):
    relation = "dbo:manager"
    reverse = True

class IsFootballTeam(FixedType):
    fixedtype = "dbo:SoccerClub"

class StadiumOf(FixedRelation):
    relation = "dbo:ground"
    reverse = True

class IsStadium(FixedType):
    fixedtype = "dbo:Stadium"
    
class CapacityOfStadium(FixedRelation):
    relation = "dbp:capacity"
    reverse = True

class CapacityOfTeam(FixedRelation):
    relation = "dbo:capacity"
    reverse = True

class TrophiesOf(FixedRelation):
    relation = "dbp:winners"

class HasParents(FixedRelation):
    relation = "dbo:parent"
    reverse = True

class HasChildren(FixedRelation):
    relation = "dbo:child"
    reverse = True

class ResidenceOf(FixedRelation):
    relation = "dbo:residence"
    reverse = True

class HasSpouse(FixedRelation):
    relation = "dbo:spouse"
    reverse = True

class CurrencyOf(FixedRelation):
    relation = "dbo:currency"
    reverse = True

class GovernmentTypeOf(FixedRelation):
    relation = "dbo:governmentType"
    reverse = True

class AssociatedActsOf(FixedRelation):
    relation = "dbo:associatedBand"
    reverse = True

class IsLanguage(FixedType):
    fixedtype = "dbo:Language"

class LanguageFamilyOf(FixedRelation):
    relation = "dbo:languageFamily"
    reverse = True

class LanguageSpokenIn(FixedRelation):
    relation = "dbo:officialLanguage"

class SpeakersOf(FixedRelation):
    relation = "dbp:speakers"
    reverse = True