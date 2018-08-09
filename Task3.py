import nltk
import json
import os

def part_of_speech(stem_words,stemmed_words_count):
    nouns = dict()  # empty  dictionary to hold all nouns
    verbs = dict()  ## empty  array to hold all verbs
    words_list = list() #list of words after removing all unnecessary things
    for key, val in stem_words.items():#iterating through the key value pair of the dictionaries
        words_list.append(val)
        remove_num = ''.join([i for i in val if i.isalpha()]) #removing all unnecesarry strings
        if len(remove_num) > 1:
            words_list.append(remove_num) #add the right strings to the list

    for word, pos in nltk.pos_tag(nltk.word_tokenize(str(words_list))):  # taking out words and word tpye pos mean part of speech var and in the mean while we tokenizing the list of words
        unwanted_slashes_are_removed = ''.join([i for i in word if i.isalpha()]) ##there were unwnated slashes which were affecting my count to avoid them i did that
        if (  pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):  # NN-->a noun , NNP--> Proper Nouns ,NNS -->Common noun plural form,  NNPS-->Proper Noun Plural Form

            if unwanted_slashes_are_removed in nouns: #refined word after removal of special char  in nouns
                nouns[unwanted_slashes_are_removed] += 1 #then simply add 1
            else:
                if unwanted_slashes_are_removed in stemmed_words_count: ##refined word after removal of special char  in stemmed word count dictionary
                      nouns[unwanted_slashes_are_removed] = stemmed_words_count[unwanted_slashes_are_removed] #then bring its count
                else:
                    nouns[unwanted_slashes_are_removed]=1 #otherwise intialize it with 1

        elif (pos == 'VBP' or pos == 'VB' or pos == 'VBZ'):  # VB --> verb , VBP --> Verb non-3rd person singular present forms,, VBZ-->Verb 3rd person singular present form
            if unwanted_slashes_are_removed in verbs: #refined word after removal of special char  in verbs
                verbs[unwanted_slashes_are_removed] += 1 #add 1 in the count of that word
            else:
                if unwanted_slashes_are_removed in stemmed_words_count:#refined word after removal of special char  in stemmed word count dictionary
                    verbs[unwanted_slashes_are_removed] = stemmed_words_count[unwanted_slashes_are_removed] #then bring its count
                else:
                    verbs[unwanted_slashes_are_removed] = 1 # if not exists intialize with 1


    return nouns, verbs
