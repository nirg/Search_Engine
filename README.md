# Search_Engine

Third year Inforamtion Retrieval Project.

A search engine for twitter tweets base on corpus of 10 million twitts Related to Corona Virus.

creates and stores inverted files (.pkl) at the Disk

Each twitt, started with parser (tokenized) which handle Emojies, Numbers ,slang ,entity , url and many more techniques.

the tokenized documents sent to  indexer which creates and stores inverted files (.pkl) at the Disk.

can choose between 6 main Search engine :

* WordNet
* Thesaurus
* Word2Vec, Word Embedding . trained model which trained on this corpus.
* GloVe ,NLP Stanford algorithm, using unsupervised learning algorithm. https://github.com/stanfordnlp/GloVe.
* spell checker,NLP Stanford algorithm.
* combination of Thesaurus and Word2Vec.

support of two ranks algorithms :

 * BM25
 * cosine similarity


# technology

Based on python 3.7
install ran.bat 
install all packages in requirements.txt file



