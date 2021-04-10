
from ranker import Ranker




class SearcherCosSim:

    def __init__(self, parser, indexer, model=None,model_1=None):
        self._parser = parser
        self._indexer = indexer
        self._ranker = Ranker()
        self._model = model
        self._model_1 = model_1


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
        query_as_list_model_1=[]
        if self._model!= None:
            query_as_list_model_1=self._model.extend_query(query_as_list)
        if self._model_1 != None:
            query_as_list_model_2 = self._model_1.extend_query(query_as_list)
            query_as_list_model_2.extend(query_as_list_model_1)
            query_as_list=query_as_list_model_2

        relevant_docs = self._relevant_docs_from_posting(query_as_list)
        relevant_docs=self._ranker.search_mechane_tf_idf(relevant_docs,query_as_list,self._indexer)
        n_relevant = len(relevant_docs)
        ranked_doc_ids = Ranker.rank_relevant_docs(relevant_docs,2000)
        return n_relevant, ranked_doc_ids

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
            if len(posting_list)>0:
                relevant_docs=self._ranker.find_mone_cos_sim(posting_list,num_of_docs,num_shows_in_query,relevant_docs)
        return relevant_docs






