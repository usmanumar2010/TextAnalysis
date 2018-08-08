import nltk
import json
import os

def part_of_speech(stem_words):
    #    dict_of_stem_words = json.loads(stemmed_words)

    nouns = dict()  # empty  dictionary to hold all nouns
    verbs = dict()  ## empty  array to hold all verbs

    words_list = list() #list of words after removing all unnecessary things


    for key, val in stem_words.items():#iterating through the key value pair of the dictionaries
        remove_num = ''.join([i for i in val if i.isalpha()]) #removing all unnecesarry strings
        if len(remove_num) > 1:
            words_list.append(remove_num) #add the right strings to the list

    for word, pos in nltk.pos_tag(nltk.word_tokenize(str(words_list))):  # taking out words and word tpye pos mean part of speech var and in the mean while we tokenizing the list of words

        if (  pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):  # NN-->a noun , NNP--> Proper Nouns ,NNS -->Common noun plural form,  NNPS-->Proper Noun Plural Form
            if word in nouns:  # checking word exist in noun dict
                nouns[word] += 1  # if exist incrementing by 1

            else:
                nouns[word] = 1 #if not exists intialize with 1

        elif (pos == 'VBP' or pos == 'VB' or pos == 'VBZ'):  # VB --> verb , VBP --> Verb non-3rd person singular present forms,, VBZ-->Verb 3rd person singular present form
            if word in verbs:  # checking word exist in verbs dict
                verbs[word] += 1  # if exist incrementing by 1
            else:
                verbs[word] = 1 #if not exists intialize with 1

    return nouns, verbs
