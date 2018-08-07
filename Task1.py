
import nltk
# download standard stop words
# write it in the documentation
# nltk.download('stopwords')

# install nltk using pip install nltk
from nltk.corpus import stopwords
import  os
from nltk.tokenize import word_tokenize
import os


# using the standard stop word list
def show_the_list_of_stop_words(book_id):
    v=os.path.dirname(os.path.abspath(__file__))
    print(v)
    stop_words = set(stopwords.words('english'))
    list=[]
    dictionary=dict()
    my_books = {'1': 'The Notebooks of Leonardo Da Vinci.txt',
                '2': 'The Outline of Science, Vol. 1 (of 4) by J. Arthur Thomson.txt',
                '3': 'The Picture of Dorian Gray by Oscar Wilde.txt',
                '4': 'Ulysses by James Joyce.txt'}

    try:
        with open(os.path.join(os.path.dirname(__file__), 'Books', my_books.get(book_id)),
                  'r') as f:  # file is opened using encoding utf-8-sig and each line is read and stored in line variable
            lines = f.readlines()
            for line in lines:
                for word in line.split():
                    word.lower()
                    if word not in stop_words:
                        list.append(word)
    except:
        with open(os.path.join(os.path.dirname(__file__), 'Books', my_books.get(book_id)),
                  'r',
                  encoding='UTF8') as f:  # file is opened using encoding utf-8-sig and each line is read and stored in line variable
            lines = f.readlines()
            for line in lines:
                for word in line.split():
                    word.lower()
                    if word not in stop_words:
                        list.append(word)


    for word in list:
        if word not in dictionary:
            dictionary[word]=word


    return dictionary


