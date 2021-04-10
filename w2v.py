
import gensim

class Word2Vec:
    def __init__(self):
        self.path=r"C:\Users\adirm\Downloads\GoogleNews-vectors-negative300.bin"
        self.model=None
        with open("inverted_index.txt", 'w', encoding="utf8") as f:
            self.model = gensim.models.KeyedVectors.load_word2vec_format(self.path, binary=True, encoding='utf-8')



    def extend_query(self,query):
        if query==None:
            return
        result=[]
        if type(query) != list and type(query) == str:
            result.append(query)
        for term in query:
            try:
                res=self.model.most_similar(term, topn=3)
                res1=res[0][0]
                res2=res[1][0]
                result.extend([term, res1, res2])
            except:
                result.append(term)
                continue
        return result

