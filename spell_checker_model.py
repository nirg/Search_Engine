

from spellchecker import SpellChecker

class Spell_check:

    def __init__(self):
        self.spell=SpellChecker()
        self.spell.word_frequency.add("coronavirus")

    def spellCheck(self, list_to_check):
        if list_to_check==None:
            return
        result = []
        if type(list_to_check)==str:
            result.append(list_to_check)
        else:
            result=list_to_check
        corrected_words_to_check =[]
        for word in result:
            corrected_word = self.spell.correction(word)
            corrected_words_to_check.append(corrected_word)

        return corrected_words_to_check