
import math
from wordnet import WordNet
from Glove import Glove
from ranker import Ranker
import utils
from spell_checker_model import Spell_check


# DO NOT MODIFY CLASS NAME
class Spell_Searcher:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit. The model
    # parameter allows you to pass in a precomputed model that is already in
    # memory for the searcher to use such as LSI, LDA, Word2vec models.
    # MAKE SURE YOU DON'T LOAD A MODEL INTO MEMORY HERE AS THIS IS RUN AT QUERY TIME.
    def __init__(self, parser, indexer, model=None,model_1=None):
        self._parser = parser
        self._indexer = indexer
        self._ranker = Ranker()
        self._model = model
        self._model_1=model_1
        self.spellcheck = Spell_check()

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def search(self, query, k=None):
        """
        Executes a query over an existing index and returns the number of
        relevant docs and an ordered list of search results (tweet ids).
        Input:
            query - string.
            k - number of top results to return, default to everything.
        Output:
            A tuple containing the number of relevant search results, and
            a list of tweet_ids where the first element is the most relavant
            and the last is the least relevant result.
        """

        query_as_list = self._parser.parse_sentence(query)
        query_as_list = self.spellcheck.spellCheck(query_as_list)
        query_as_list_model_1=query_as_list
        if (self._model != None):
            query_as_list_model_1 = self._model.extend_query(query_as_list)

        if (self._model_1 != None):
            query_as_list_model_2 = self._model_1.extend_query(query_as_list)
            query_as_list_model_1.extend(query_as_list_model_2)


        query_as_list=query_as_list_model_1

        docs_dict = self._indexer.get_docs_dict()
        relevant_docs,query_dict = self._relevant_docs_from_posting(query_as_list)
        if relevant_docs==None or len(relevant_docs)==0:
            return 0,[]

        relevant_docs1=self._ranker.BM25(relevant_docs,query_as_list,docs_dict,query_dict)
        n_relevant = len(relevant_docs1)
        ranked_doc_ids = Ranker.rank_relevant_docs(relevant_docs1,2000)
        return n_relevant, ranked_doc_ids





    # feel free to change the signature and/or implementation of this function
    # or drop altogether.
    def _relevant_docs_from_posting(self, query_as_list):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query_as_list: parsed query tokens
        :return: dictionary of relevant documents mapping doc_id to document frequency.
        """
        query_dict = {}
        for t in query_as_list:
            if t not in query_dict:
                query_dict[t] = query_as_list.count(t)

        relevant_docs={}
        for term in query_dict:
            posting_list = self._indexer.get_term_posting_list(term)
            num_shows_docs=len(posting_list)
            for doc in posting_list:
                doc_id=doc[0]
                freq_in_doc=doc[1]

                info_lst=[term, freq_in_doc,num_shows_docs]
                if(doc_id not in relevant_docs):
                    relevant_docs[doc_id]=[info_lst]
                else:
                    relevant_docs[doc_id].append(info_lst)

        return relevant_docs,query_dict











