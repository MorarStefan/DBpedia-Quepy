from refo import Plus, Question
from quepy.dsl import HasKeyword
from quepy.parsing import Lemma, Lemmas, Pos, QuestionTemplate, Particle
from dsl import IsLanguage, LanguageFamilyOf, LabelOf, LanguageSpokenIn, SpeakersOf
from synonyms import Synonyms

synonyms_ref = Synonyms() 

language = (Pos("JJ") + Pos("JJ")) | (Question(Pos("JJ")) + Question(Pos("NN") | Pos("NNP") | Pos("NNS") | Pos("NNPS"))) 

class Language(Particle):
    regex = language

    def interpret(self, match):
        return IsLanguage() + HasKeyword(match.words.tokens)

class LanguageFamilyOfQuestion(QuestionTemplate):
    """
    Ex: "What type of language is Romanian language?"
        "What is the language family of French language?"
    """
    type_wordnet = synonyms_ref.getLemmaPreposition("type", 'n') | Lemma("family")
    regex = (Pos("WP") + Question(type_wordnet + Pos("IN")) + Lemmas("language be") + Language() + Question(Pos("."))) | \
            (Pos("WP") + Question(Lemma("be")) +  Question(Pos("DT")) + Lemma("language") + type_wordnet + Pos("IN") + Language() + Question(Pos(".")))

    def interpret(self, match):
        language = LanguageFamilyOf(match.language)
        language_name = LabelOf(language)
        return  language_name, "enum"


class WhereIsSpokenQuestion(QuestionTemplate):
    """
    Ex: "Where is Romanian language the official language?"
        "Where is Indian English spoken?"
        "Enumerate countries speaking German language"
    """
    
    list_wordnet = synonyms_ref.getLemmaPreposition("list", 'v')
    regex = (Lemmas("where be") + Question(Pos("DT")) + Language() + Question(Pos("DT")) + Lemmas("official language") + Question(Pos("."))) | \
            (Lemmas("where be") + Question(Pos("DT")) + Language() + Lemma("speak") + Question(Pos("."))) | \
            (Question(list_wordnet) + Question(Pos("NN") | Pos("NNP") | Pos("NNS")) + Lemma("speak") + Language() + Question(Pos(".")))
    
    def interpret(self, match):
        language = LanguageSpokenIn(match.language)
        language_name = LabelOf(language)
        return  language_name, "enum"

class HowManySpeakLanguageQuestion(QuestionTemplate):
    """
    Ex: "How many speak English language?"
        "How many people speak French language?"
        "Number of people speaking German language"
        "People speaking Canadian French"
    """

    people_wordnet = synonyms_ref.getLemmaPreposition("people", 'n')
    regex = (Lemmas("how many") + Question(people_wordnet) + Lemma("speak") + Language() + Question(Pos("."))) | \
            (Question(Lemma("number") + Pos("IN")) + people_wordnet + Lemma("speak") + Language() + Question(Pos(".")))

    def interpret(self, match):
        number = SpeakersOf(match.language)
        return  number, "literal"