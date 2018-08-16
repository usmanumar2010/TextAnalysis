
import nltk
# download standard stop words
# write it in the documentation
# nltk.download('stopwords')

from nltk.corpus import stopwords
import  os
from nltk.tokenize import word_tokenize
import os


# using the standard stop word list
def show_the_list_of_stop_words(book_id):
    stop_words = set(stopwords.words('english')) #intializing stop words with english
    list=[] #list that will contain all stop words
    dictionary=dict() #dictionary that will help to make a json type structure
    lines="" #that will contain all book lines
    #my books contains all books
    my_books = {'1': 'The Notebooks of Leonardo Da Vinci.txt',
                '2': 'The Outline of Science, Vol. 1 (of 4) by J. Arthur Thomson.txt',
                '3': 'The Picture of Dorian Gray by Oscar Wilde.txt',
                '4': 'Ulysses by James Joyce.txt'}

    try:
        with open(os.path.join(os.path.dirname(__file__), 'Books', my_books.get(book_id)),
                  'r') as f:  # if the file opened without mentioning encoding then proceed
            lines = f.readlines() #reading all lines

    except:
        with open(os.path.join(os.path.dirname(__file__), 'Books', my_books.get(book_id)),
                  'r',
                  encoding='ISO-8859-1') as f:  # file is opened using encoding utf-8-sig
            lines = f.readlines() #reading all lines

    for line in lines:  # reading each line
        for word in line.split():  # spliting each line
            word.lower()  # convert to lower case each word
            if word not in stop_words:  # checking if word is not a stop word
                remove_special_char = ''.join([i for i in word if i.isalpha()])
                list.append(remove_special_char)  # making a list of all those words which are not stop words
    for word in list:  #iterating list
        if word not in dictionary: #seeing each word in dictionary
            dictionary[word]=word #if word not present then place it in a dict


    return dictionary  #return dictionary


