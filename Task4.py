import gensim
import  nltk
from nltk.tokenize import word_tokenize
import operator
import  os


def sentence_similarity(first_book,second_book):
    my_books={'1':'The Notebooks of Leonardo Da Vinci.txt','2':'The Outline of Science, Vol. 1 (of 4) by J. Arthur Thomson.txt','3':'The Picture of Dorian Gray by Oscar Wilde.txt','4':'Ulysses by James Joyce.txt'}

    lines=""
    try:
         with open(os.path.join(os.path.dirname(__file__), 'Books', my_books.get(first_book)),
              'r') as f:
              lines=lines+str(f.readlines()) #all file will store in lines
    except:
         with open(os.path.join(os.path.dirname(__file__), 'Books', my_books.get(first_book)),
              'r',
             encoding='ISO-8859-1') as f:  # file is opened using encoding utf-8-sig and each line is read and stored in line variable
              lines = lines + str(f.readlines())#all file will in lines variable
    sentences = nltk.sent_tokenize(lines) # tokenizing document using nltk into sentences
    gen_docs = [[ "".join(filter(str.isalpha,w.lower()))  for w in word_tokenize(text)] # list of sentences with each sentences is list of tokens word_tokenzie()--> provides listof tokens
                for text in sentences]
    dictionary = gensim.corpora.Dictionary(gen_docs) # converting the list of tokens into dictionary
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs] # A corpus is a list of bags of words. A bag-of-words representation for a document just lists the number of times each word occurs in the document.
    tf_idf = gensim.models.TfidfModel(corpus) #a tf-idf model from the corpus. Note that num_nnz is the number of tokens.
    sims = gensim.similarities.Similarity(os.path.join(os.path.dirname(__file__), '.'), tf_idf[corpus],num_features=len(dictionary)) #tf-idf stands for term frequency-inverse document frequency. Term frequency is how often the word shows up in the document and inverse document fequency scales the value by how rare the word is in the corpus.


    #for second book
    second_book_lines=""

    count=0
    try:

        with open(os.path.join(os.path.dirname(__file__), 'Books', my_books.get(second_book)),
              'r') as f:
          if(count<200):
             second_book_lines=second_book_lines+str(f.readlines()) #storing all lines of book in lines variable
    except:
        count=0
        with open(os.path.join(os.path.dirname(__file__), 'Books', my_books.get(second_book)),
              'r',encoding='ISO-8859-1') as f:  # file is opened using encoding utf-8-sig and each line is read and stored in line variable
          if(count<200):
             second_book_lines=second_book_lines+str(f.readlines())
    sentences_second_book = nltk.sent_tokenize(second_book_lines) # tokenizing document using nltk into sentences

    score_of_each_sent=[]#a list that will contain the score of each sentence in a list
    for one_by_one_sentence in sentences_second_book:
        query_doc = [w.lower() for w in word_tokenize(one_by_one_sentence)] #string is user inputed sentence. tokenzing the sentence
        query_doc_bow = dictionary.doc2bow(query_doc) # create tuple of above tokenized string in the form of i.e [(1,2),(2,3),(3,4)]
        query_doc_tf_idf = tf_idf[query_doc_bow] #get tokens which are significant ,using this we can find sentence is similar to which sentence
        index, value = max(enumerate(sims[query_doc_tf_idf]), key=operator.itemgetter(1)) #getting the index ,value of maximum token for most similar sentence
        score_of_each_sent.append(round(value, 1)) #rounding the decimal no upto one number after a decimal



    add_score_of_sent=0.0
    for s in score_of_each_sent:  #iterating through each sentence score
         add_score_of_sent=s+add_score_of_sent #add each sentence score later will compute the percentage with it

    return  ((add_score_of_sent/len(sentences_second_book))*100)  #calculating the percentage score of similarity and returing it