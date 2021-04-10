
import math
import numpy as np


class Ranker:
    def __init__(self):
        pass

    @staticmethod
    def rank_relevant_docs(relevant_docs, k=None):
        """
        This function provides rank for each relevant document and sorts them by their scores.
        The current score considers solely the number of terms shared by the tweet (full_text) and query.
        :param k: number of most relevant docs to return, default to everything.
        :param relevant_docs: dictionary of documents that contains at least one term from the query.
        :return: sorted list of documents by score
        """
        ranked_results = sorted(relevant_docs.items(), key=lambda item: item[1], reverse=True)
        if k is not None:
            ranked_results = ranked_results[:k]
        return [d[0] for d in ranked_results]

    def find_mone_cos_sim(self,posting_list, num_of_docs,num_shows_in_query,relevant_docs):
        """
        this function calculate the numerator of cos_sim
        :param posting_list: posting list of the term
        :param num_of_docs: num docs in corpus
        :param num_shows_in_query:
        :param relevant_docs:
        :return:
        """
        term_num_of_shows = len(posting_list)
        idf = num_of_docs / term_num_of_shows
        for doc in posting_list:
            doc_num = doc[0]
            trem_freq = doc[1]
            tf = doc[2]
            tf_idf_Wiq = tf * idf * num_shows_in_query
            if doc_num not in relevant_docs:
                relevant_docs[doc_num] = tf_idf_Wiq
            else:
                relevant_docs[doc_num] += tf_idf_Wiq

        return relevant_docs

    def search_mechane_cos_sim(self, relevant_docs, query,indexer):
        """

        :param relevant_docs: the relevants docs for the given query
        :param query:
        :param indexer: the indexet instance
        :return: the total of cos_sim
        """
        Wiq = 0
        query_dict = {}
        for t in query:
            if t not in query_dict:
                query_dict[t] = query.count(t)
        for term in query_dict:
            Wiq += (query_dict[term]) ** 2

        dict_docs = indexer.get_docs_dict()  # Dictionary
        num_of_docs = len(dict_docs)
        for doc in relevant_docs:
            Wij = 0
            terms_lst = dict_docs[doc]  # list of tuples
            for term in terms_lst:
                term_name = term[0]
                term_tf = term[1]
                num_shows = indexer.get_num_of_term_in_docs(term_name)
                if (num_shows == 0):
                    continue
                idf = num_of_docs / num_shows
                Wij += (term_tf * idf) ** 2

            relevant_docs[doc] = relevant_docs[doc] / math.sqrt(Wij * Wiq)

        return relevant_docs


    def BM25(self,relevant_docs,query_as_list,docs_dict,query_dict, k=1.5, b=0.75):
        """
        :param relevant_docs: the relevants docs for the given query
        :param query_as_list: tokenized query
        :param docs_dict: dictionary with information about the docs in corpus
        :param query_dict: dictionary with the terms in query and num of instance of each of them

        :return: docs dictionary with their score from the rank
        """

        score_docs_dict={}
        num_of_docs_total=len(docs_dict)
        total_docs_length=0
        for doc in relevant_docs:
            doc_len1 = docs_dict[doc][0][2]
            total_docs_length+=doc_len1
        avg_doc_len=total_docs_length/len(relevant_docs)


        for doc in relevant_docs:
            doc_len=docs_dict[doc][0][2]
            for term in relevant_docs[doc]:
                term_name=term[0]
                term_freq_in_doc=term[1]
                num_shows_docs=term[2]
                num_shows_in_query=query_dict[term_name]

                idf_qi=np.log10(((num_of_docs_total-num_shows_docs+0.5)/(num_shows_docs+0.5))+1)
                mone= term_freq_in_doc*(k+1)
                mechane = term_freq_in_doc +k*(1-b+b*(doc_len/avg_doc_len))

                if doc not in score_docs_dict:
                    score_docs_dict[doc]= idf_qi*(mone/mechane)
                else:
                    score_docs_dict[doc] += idf_qi * (mone / mechane)

        return score_docs_dict




