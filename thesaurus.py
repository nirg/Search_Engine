from nltk.corpus import lin_thesaurus

class Thesaurus:
    def __init__(self):
        c=""

    def extend_query(self,query):
        if query==None:
            return
        result=[]
        if type(query) != list and type(query) == str:
            result.append(query)

        for term in query:
            res=lin_thesaurus.scored_synonyms(term, fileid="simN.lsp")
            sort_res=sorted(res, key = lambda x: x[1], reverse=True)
            try:
                result.extend([term,sort_res[0][0],sort_res[1][0]])
            except:
                result.append(term)
                continue
        return result






#scored_synonyms = lin_thesaurus.scored_synonyms(term, fileid="simN.lsp")
#        best_2 = sorted(scored_synonyms, key = lambda x: x[1], reverse=True)[:2]
#        best_2_list = [tup[0] for tup in best_2]