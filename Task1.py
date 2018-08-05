
import nltk
# download standard stop words
# write it in the documentation
# nltk.download('stopwords')

# install nltk using pip install nltk
from nltk.corpus import stopwords
import  os
from nltk.tokenize import word_tokenize



# using the standard stop word list
def show_the_list_of_stop_words():
    import os
    v=os.path.dirname(os.path.abspath(__file__))
    print(v)
    stop_words = set(stopwords.words('english'))
    list=[]
    dictionary=dict()
    with open(os.path.join(os.path.dirname(__file__), 'Books', 'The Notebooks of Leonardo Da Vinci.txt'), 'r') as f:  # file is opened using encoding utf-8-sig and each line is read and stored in line variable
        lines=f.readlines()
        for line in lines:
            for word in line.split():
                word.lower()
                if word not in stop_words :
                    list.append(word)
    for word in list:
        if word not in dictionary:
            dictionary[word]=word

     # d=[for word in list if word in dictionary dictionary[word]+=1 else dictionary[word]=1]
      #  list=[word for line in lines for word in line.split()  if  word not in stop_words]


        # for word in lines.split():  # words are split from each line
        #     word = word.lower()  # words are tranformed into lower format i.e Apple would be turned into apple to make sure case sensitive words are consider same
        #     if not word in stop_words:
        #         list=list+word
    return dictionary


