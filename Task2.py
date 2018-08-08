from nltk.stem.snowball import SnowballStemmer
import os

def stemming(book_id):
    # the stemmer
    stemmer = SnowballStemmer('english') #intiallizing snowball stemmer
    list = [] #list containg all stemmed words
    dictionary1 = dict() #containing only stemmed word list
    dictionary2 = dict() #containing stemmed words with there count
    lines = "" #all lines of a book will come in it

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
                  encoding='UTF8') as f:  # file is opened using encoding utf-8-sig
            lines = f.readlines()#reading all lines

    for line in lines:  # reading each line
        for word in line.split():  # spliting each line
            word.lower()  # converting word to lower casw
            list.append(stemmer.stem(word))  # stemmed the word and it it to a list
    for word in list:# first dictionary which will contain stemmed word and there count
        if word not in dictionary1:
            dictionary1[word] = 1  #if the word is not present the intialize it with 1
        else:
            dictionary1[word] += 1   #else keep on adding 1 in its count

    # second dictinary of stemmed words
    for word in list:
        if word not in dictionary2:
            dictionary2[word] = word #creatind dictionary of stemmed words that we will use later
    # returning two as one will display count against the word and the dictionay will have all stemmed words list that we will use in task3
    return dictionary1, dictionary2
