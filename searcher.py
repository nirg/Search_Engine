import math
from word2vec import Word2Vec
from Glove import Glove
from ranker import Ranker
import utils


# DO NOT MODIFY CLASS NAME
class Searcher:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit. The model
    # parameter allows you to pass in a precomputed model that is already in
    # memory for the searcher to use such as LSI, LDA, Word2vec models.
    # MAKE SURE YOU DON'T LOAD A MODEL INTO MEMORY HERE AS THIS IS RUN AT QUERY TIME.
    def __init__(self, parser, indexer, model=None):
        self._parser = parser
        self._indexer = indexer
        self._ranker = Ranker()
        self._model = model

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
        if(self._model!= None):
            print(self._model)
            query_as_list=self._model.extend_query(query_as_list)

        relevant_docs = self._relevant_docs_from_posting(query_as_list)
        relevant_docs=self.search_mechane(relevant_docs,query_as_list)
        n_relevant = len(relevant_docs)
        ranked_doc_ids = Ranker.rank_relevant_docs(relevant_docs,2000)
        return n_relevant, ranked_doc_ids

   #def extand_query_by_model(self,query_as_list):
   #    if type(self._model) is Glove:
   #        glove = Glove()
   #        query=glove.extend_query(query_as_list)
   #        return query
   #    elif type(self._model) is Word2Vec:
   #        Word2Vec=()
   #

    def search_mechane(self,relevant_docs,query):

        Wiq=0
        query_dict = {}
        for t in query:
            if t not in query_dict:
                query_dict[t] = query.count(t)
        for term in query_dict:
            Wiq+=(query_dict[term])**2

        dict_docs=self._indexer.get_docs_dict() # Dictionary
        num_of_docs = len(dict_docs)
        for doc in relevant_docs:
            Wij = 0
            terms_lst=dict_docs[doc] # list of tuples
            for term in terms_lst:
                term_name=term[0]
                term_tf= term[1]
                num_shows=self._indexer.get_num_of_term_in_docs(term_name)
                if(num_shows==0):
                    continue
                idf=num_of_docs/num_shows
                Wij+=(term_tf*idf)**2

            relevant_docs[doc]=relevant_docs[doc]/math.sqrt( Wij*Wiq )

        return relevant_docs


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

        relevant_docs = {}
        docs_dict = self._indexer.get_docs_dict()
        num_of_docs=len(docs_dict)
        for term in query_dict:
            num_shows_in_query=query_dict[term]
            posting_list = self._indexer.get_term_posting_list(term)
            if(len(posting_list)>0):
                term_num_of_shows=len(posting_list)
                idf = num_of_docs/term_num_of_shows
                for doc in posting_list:
                    doc_num  = doc[0]
                    trem_freq = doc[1]
                    tf = doc[2]
                    tf_idf_Wiq = tf*idf*num_shows_in_query
                    if doc_num not in relevant_docs:
                        relevant_docs[doc_num]=tf_idf_Wiq
                    else:
                        relevant_docs[doc_num] += tf_idf_Wiq
        return relevant_docs






