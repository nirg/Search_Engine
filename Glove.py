from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models import KeyedVectors
from parser_module import Parse

class Glove:

    def __init__(self):
        self.input_file = r"C:\Users\adirm\Downloads\glove.twitter.27B.25d.txt"   #'../../../../glove.twitter.27B.25d.txt'
        self.output_file = 'glove.twitter.27B.25d.txt.word2vec'
        glove2word2vec(self.input_file, self.output_file)
        self.model=KeyedVectors.load_word2vec_format(self.output_file, binary=False)

    def extend_query(self, query):
        if query==None:
            return None
        result = []
        if type(query)!=list and type(query)==str:
            result.append(query)
        for term in query:
                try:
                    result.extend([term,self.model.most_similar(term)[0][0], self.model.most_similar(term)[1][0]])
                except:
                    result.append(term)
                    continue
        return result
