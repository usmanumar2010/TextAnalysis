from nltk.stem.snowball import SnowballStemmer
import os

def stemming():
    # the stemmer
    stemmer = SnowballStemmer('english')

    list = []
    dictionary1 = dict()
    dictionary2 = dict()
    with open(os.path.join(os.path.dirname(__file__), 'Books', 'The Notebooks of Leonardo Da Vinci.txt'),
              'r') as f:  # file is opened using encoding utf-8-sig and each line is read and stored in line variable
        lines = f.readlines()
        for line in lines:
            for word in line.split():
                word.lower()
                list.append(stemmer.stem(word))
    # first dictionary of count
    for word in list:
        if word not in dictionary1:
            dictionary1[word] = 1
        else:
            dictionary1[word] += 1

    # second dictinary of stemmed words
    for word in list:
        if word not in dictionary2:
            dictionary2[word] = word
    # returning two as one will display count against the word and the dictionay will have all stemmed words that we will use in task3
    return dictionary1, dictionary2
