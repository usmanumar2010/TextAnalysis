import nltk
import json
import os

def part_of_speech(stem_words):
    #    dict_of_stem_words = json.loads(stemmed_words)

    nouns = dict()  # empty  dictionary to hold all nouns
    verbs = dict()  ## empty  array to hold all verbs

    words_list = list()


    for key, val in stem_words.items():
        remove_num = ''.join([i for i in val if i.isalpha()])
        if len(remove_num) > 1:
            words_list.append(remove_num)

    for word, pos in nltk.pos_tag(nltk.word_tokenize(str(words_list))):  # taking out words and word tpye we

        if (  pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):  # NN-->a noun , NNP--> Proper Nouns ,NNS -->Common noun plural form,  NNPS-->Proper Noun Plural Form
            if word in nouns:  # checking word exist in noun dict
                nouns[word] += 1  # if exist incrementing by 1

            else:
                nouns[word] = 1

        elif (pos == 'VBP' or pos == 'VB' or pos == 'VBZ'):  # VB --> verb , VBP --> Verb non-3rd person singular present forms,, VBZ-->Verb 3rd person singular present form
            if word in verbs:  # checking word exist in verbs dict
                verbs[word] += 1  # if exist incrementing by 1
            else:
                verbs[word] = 1

    return nouns, verbs
