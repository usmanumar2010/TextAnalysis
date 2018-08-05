import gensim
import  nltk
from nltk.tokenize import word_tokenize
import operator

def sentence_similarity(book,string):

    try:
        File = open('Books/'+book,encoding = "ISO-8859-1")  # open file
    except:
        File = open('Books/' + book, encoding=None)
    lines = File.read()  # read all lines

    sentences = nltk.sent_tokenize(lines) # tokenizing document using nltk into sentences
    gen_docs = [[ "".join(filter(str.isalpha,w.lower()))  for w in word_tokenize(text)] # list of sentences with each sentences is list of tokens word_tokenzie()--> provides listof tokens
                for text in sentences]
    dictionary = gensim.corpora.Dictionary(gen_docs) # converting the list of tokens into dictionary
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs] # A corpus is a list of bags of words. A bag-of-words representation for a document just lists the number of times each word occurs in the document.
    tf_idf = gensim.models.TfidfModel(corpus) #a tf-idf model from the corpus. Note that num_nnz is the number of tokens.


    sims = gensim.similarities.Similarity('Books/', tf_idf[corpus],num_features=len(dictionary)) #tf-idf stands for term frequency-inverse document frequency. Term frequency is how often the word shows up in the document and inverse document fequency scales the value by how rare the word is in the corpus.
    query_doc = [w.lower() for w in word_tokenize(string)] #string is user inputed sentence. tokenzing the sentence
    query_doc_bow = dictionary.doc2bow(query_doc) # create tuple of above tokenized string in the form of i.e [(1,2),(2,3),(3,4)]
    query_doc_tf_idf = tf_idf[query_doc_bow] #get tokens which are significant ,using this we can find sentence is similar to which sentence

    index, value = max(enumerate(sims[query_doc_tf_idf]), key=operator.itemgetter(1)) #getting the index ,value of maximum token for most similar sentence
    min_index, min_value = min(enumerate(sims[query_doc_tf_idf]), key=operator.itemgetter(1))#getting the index ,value of minimum token for most similar sentence

    print(sum(sims[query_doc_tf_idf]))
    return (sentences[index],sentences[min_index]) # getting similar and dissimilar sentece using above indexes