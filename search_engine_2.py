import os
import shutil
from pathlib import Path

import pandas as pd
from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import utils
from word2vec import Word2Vec

# DO NOT CHANGE THE CLASS NAME
class SearchEngine:

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation, but you must have a parser and an indexer.
    def __init__(self, config=None):
        self._config = config
        self._parser = Parse(config)
        self._indexer = Indexer(config)
        self._model = Word2Vec()

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def build_index_from_parquet(self, fn):
        """
        Reads parquet file and passes it to the parser, then indexer.
        Input:
            fn - path to parquet file
        Output:
            No output, just modifies the internal _indexer object.
        """
        df = pd.read_parquet(fn, engine="pyarrow")
        documents_list = df.values.tolist()
        # Iterate over every document in the file
        number_of_documents = 0
        for idx, document in enumerate(documents_list):
            # parse the document
            parsed_document = self._parser.parse_doc(document)
            number_of_documents += 1
            # index the document data
            self._indexer.add_new_doc(parsed_document)
        print('Finished parsing and indexing.')
        self._indexer.save_index("bench_idx")
       # lst=self._indexer.load_index("bench_idx")
       # print("the length of inverted index : "+str(len(lst[0])))
       # print("the length of posting file : " + str(len(lst[1])))
       # print("number document in the corpus : " + str(len(lst[2])))





       # for i in range(len(doc_list)):
       #     tmp_list = r.read_file(file_name=doc_list[i])
       #     for idx, document in enumerate(tmp_list):
       #         number_of_documents += 1
       #         parsed_document = p.parse_doc(document, stemming)
       #         if (number_of_documents % 1000000 == 0):
       #             p.get_entity_dict()
       #             indexer.update_index_data(p.get_global_dict(), p.get_posting_dict())
       # if (len(p.global_dict) > 0):
       #     p.get_entity_dict()
       #     indexer.update_index_data(p.get_global_dict(), p.get_posting_dict())
       # indexer.merge_all_posts_dict()



    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_index(self, fn):
        """
        Loads a pre-computed index (or indices) so we can answer queries.
        Input:
            fn - file name of pickled index.
        """
        self._indexer.load_index(fn)

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_precomputed_model(self, model_dir=None):
        """
        Loads a pre-computed model (or models) so we can answer queries.
        This is where you would load models like word2vec, LSI, LDA, etc. and
        assign to self._model, which is passed on to the searcher at query time.
        """
        x=5


        # DO NOT MODIFY THIS SIGNATURE
        # You can change the internal implementation as you see fit.

    def search(self, query):
        """
        Executes a query over an existing index and returns the number of
        relevant docs and an ordered list of search results.
        Input:
            query - string.
        Output:
            A tuple containing the number of relevant search results, and
            a list of tweet_ids where the first element is the most relavant
            and the last is the least relevant result.
        """
        searcher = Searcher(self._parser, self._indexer, model=self._model)
        return searcher.search(query)


    def move_to_output(self,output):
        '''
        this function move the posting dicts to the output path
        :param output:
        :return:
        '''



#ef main(corpus_path, output_path, stemming, queries, num_docs_to_retrieve):
#   '''
#   corpus_path - the path to the corpus
#   output_path - the path of the posting files will be save
#   stemming - True if user want stemming , otherwise False
#   queries- can be list with the queries inside or can be a text file with the queries
#   num_docs_to_retrieve .
#   '''
#   run_engine(corpus_path,output_path,stemming)
#   data_list=[]
#   if(type(queries)!=list):
#       queries=read_query_txt(queries)
#   for i in range(len(queries)):
#       for doc_tuple in search_and_rank_query(queries[i],num_docs_to_retrieve):
#           print('Tweet id: {} Score: {}'.format({doc_tuple[0]}, {doc_tuple[1]}))
#           data_list.append(["query: "+str(i),doc_tuple[0],doc_tuple[1]])
#       with open('results.csv', 'w', newline='') as file:
#           writer = csv.writer(file, delimiter='|')
#           writer.writerows(data_list)
#   move_to_output(output_path)












def main():
    config=ConfigClass()
    engine=SearchEngine(config)
    engine.build_index_from_parquet(config.get__corpusPath())
    # x,y=engine.search("donald trump")
    queries = pd.read_csv(os.path.join('data', 'queries_train.tsv'), sep='\t')
    z=5
    lst=[]

    for query in queries.values:
        lst.append((query[0],query[1]))
        x, y = engine.search(query[1])
        print("num of query: "+str(query[0])+" num of result: "+str(x))








