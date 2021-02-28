
from nltk.corpus import wordnet   #Import wordnet from the NLTK
#
class Word2Vec:
   def __init__(self):
       self.name=""

   def extend_query(self,query):

      if query==None:
          return
      ext_query=[]
      for term in query:
          syn = set()
          ant = set()
          synsets=wordnet.synsets(term)
          if len(synsets)==0:
              continue
          syn1=synsets[0]

          for synset in synsets:
              for lemma in synset.lemmas():
                  syn2=wordnet.synsets(lemma.name())[0]
                  similarly=syn1.wup_similarity(syn2)
                  if type(similarly) is float and similarly > 0.7:
                    syn.add(lemma.name())  # add the synonyms
                  if lemma.antonyms():  # When antonyms are available, add them into the list
                      ant.add(lemma.antonyms()[0].name())
          ext_query+=syn
         # ext_query=self.add_to_result(ext_query,syn,term)
      return ext_query


   def add_to_result(self,ext_query,syn,term):
       count = 0
       for i in range(len(syn)):
           if count >= 2:
               break
           else:
               if (syn[i] != term):
                   ext_query.append(syn[i])
                   count += 1
       return ext_query

  #    syn = set()
  #    ant = set()
  #    x = wordnet.synsets("tree")
  #    syn1 = x[0]
  #    for synset in x:
  #        for lemma in synset.lemmas():  # add the synonyms
  #            syn2 = wordnet.synsets(lemma.name())[0]
  #            similarity = syn1.wup_similarity(syn2)
  #            if type(similarity) is float and similarity > 0.7:
  #                syn.add(lemma.name())
  #            if lemma.antonyms():  # When antonyms are available, add them into the lis
  #                ant.add(lemma.antonyms()[0].name())







#syn = list()
#ant = list()
#for synset in wordnet.synsets("bad"):
#   for lemma in synset.lemmas():
#      syn.append(lemma.name())    #add the synonyms
#      if lemma.antonyms():    #When antonyms are available, add them into the list
#        ant.append(lemma.antonyms()[0].name())
#print('Synonyms: ' + str(syn[0:7]))