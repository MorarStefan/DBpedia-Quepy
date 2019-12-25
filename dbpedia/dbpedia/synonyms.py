from nltk.corpus import wordnet
from quepy.parsing import Lemma, Lemmas

class Synonyms: 
    def findSynonyms(self, word, speech_part):
        synonyms = []

        for syn in wordnet.synsets(word, pos = speech_part):
            for l in syn.lemmas():
                synonyms.append(l.name().replace("_", " "))
            for hyper in syn.hypernyms():
                for l in hyper.lemmas():
                    synonyms.append(l.name().replace("_", " "))
    
        return synonyms
    
    def applyLemma(self, word):
        if(' ' in word):
            return Lemmas(word)
        return Lemma(word)

    def getLemmaPreposition(self, word, speech_part):
        synonyms = self.findSynonyms(word, speech_part)

        topic = self.applyLemma(synonyms[0])

        n = len(synonyms)
        i = 1
        while i < n:
            topic |= self.applyLemma(synonyms[i])
            i += 1
        
        return topic
