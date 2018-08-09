import json
import sys

from flask import Flask
from pymongo import MongoClient
from collections import Counter

sys.path.append("./Questions/")
import Task2
import Task1
import Task3
import Task4
from nltk.stem.snowball import SnowballStemmer

# sys.path.append("/Questions/Task1.py")

app = Flask(__name__)

# configration ,instantiate database connection object
client = MongoClient('localhost', 27017)

db = client.text_analysis



#routes
@app.route("/")
def hello():

    return "Welcome to Connectavo"


@app.route("/refined_book/")
@app.route("/refined_book/<book_id>")
def refined_book(book_id='all'):
    if book_id == '1' or book_id == '2' or book_id == '3' or book_id == '4':
        query = db.processed_text.find_one({'book_id': book_id})#query if data present against the book_id
        if query: #if something come in the response
            if query["words"]:  # if the response contains words
                words_json = query["words"]  #load the json of words in the word_json variable
                return  words_json  #return the word_json which has the words
            else:  # if there is a document present but there is a no value against query["words"]
                data = Task1.show_the_list_of_stop_words(book_id)  #trigger the function of to get the refined text without stop words
                updateQueryTask1(book_id,data)  #as the document present so just update the value against the book id words
                return  json.dumps(data) #return the json words json
        else: #if the query is empty no document is present relative to the book id
            words_are = Task1.show_the_list_of_stop_words(book_id)  #trigger the function in the task1 to get the refind words
            insertQueryTask1(book_id, words_are) #inset the document in the database
            return json.dumps(words_are) #return the json of words
    elif book_id == 'ALL' or book_id == 'all':
        my_dict = {} #create the dictionary that will contain sum of all the other dictionaries against book id
        list_of_all_books = ['1', '2', '3', '4'] #list of all books ids
        for book_no in list_of_all_books:  #one by one iterating each book
            query = db.processed_text.find_one({'book_id': book_no}) #querying if data present against that book id
            if query: #if some document is present against the book id
                if query["words"]:  # checking if the cotains any value against words key
                    words_dict = json.loads(query["words"]) #load converting that word json into dictionary
                else:  # if document is present but there is value against words key
                    words_dict = Task1.show_the_list_of_stop_words(book_no)  # triggering function in task1 file to get words dictionary
                    updateQueryTask1(book_no, words_dict)  # as the document present so just update the value against the book id words
            else:
                words_dict = Task1.show_the_list_of_stop_words(book_no)##trigger the function in the task1 to get the refind words
                insertQueryTask1(book_no, words_dict)#inset the document in the database
            my_dict[book_no] = words_dict #placing the dictionaries in the main dictionary so later we can view the words against book id
        return json.dumps(my_dict)  #returning the json containing all the dictionaries
    return "Books only from 1 to 4"

@app.route("/stemmed_lemmatized/")
@app.route("/stemmed_lemmatized/<book_id>")
def stemmed_lemmatized(book_id='all'):
    if book_id == '1' or book_id == '2' or book_id == '3' or book_id == '4':
        query = db.processed_text.find_one({'book_id': book_id})#query if data present against the book_id
        if query:#if something come in the response
            if query["stemmed_words_count"]:  # if the response contains  the count of every stemmed_word
                stemmed_words_count = query["stemmed_words_count"] #load the json of stemmed_words in the stemmed_words_count variable
                return  stemmed_words_count #return the stemmed_word_count json which has the words
            else:  # if document is present but there is value against words key
                stemmed_words_count, stemmed_words = Task2.stemming(book_id)   #trigger the function of to get the stemmed_words and stemmed words count
                updateQueryTask2(book_id, stemmed_words,stemmed_words_count)  # as the document present so just update the value against the book id words
                return  json.dumps(stemmed_words_count)#return the json words json
        else:#if the query is empty no document is present relative to the book id
            stemmed_words_count, stemmed_words = Task2.stemming(book_id)#trigger the function in the task2 to get the stemmed words and stemmed words count
            insetQueryTask2(book_id, stemmed_words, stemmed_words_count) #inset the document in the database
            return  json.dumps(stemmed_words_count) #return the json of stemmed words count
    elif book_id == 'all' or book_id == 'ALL':
        my_dict = {}  #create the dictionary that will contain count all stemmed words
        list_of_all_books = ['1', '2', '3', '4'] #list of all books ids
        for book_no in list_of_all_books: #one by one iterating each book
            query = db.processed_text.find_one({'book_id': book_no}) #query if data present against the book_id
            if query:#if something come in the response
                if query["stemmed_words_count"]:  # if the response contains  the count of every stemmed_word
                    stemmed_words_count = json.loads(query["stemmed_words_count"]) #load the json of stemmed_words in the stemmed_words_count variable
                else: #if the query is empty no document is present relative to the book id
                    stemmed_words_count, stemmed_words = Task2.stemming(
                        book_no)  #trigger the function of to get the stemmed_words and stemmed words count
                    updateQueryTask2(book_no, stemmed_words,
                                     stemmed_words_count)   # as the document present so just update the value against the book id words
            else:#if the query is empty no document is present relative to the book id
                stemmed_words_count, stemmed_words = Task2.stemming(book_no)#trigger the function in the task2 to get the stemmed words and stemmed words count
                insetQueryTask2(book_no, stemmed_words, stemmed_words_count)#inset the document in the database
            my_dict = Counter(my_dict) + Counter(stemmed_words_count) #Counter will take the intersection of the keys that common and its values otherwise union
        return json.dumps(my_dict) #return the json of stemmed words count
    return "Books only from 1 to 4"


@app.route("/part_of_speech/")
@app.route("/part_of_speech/<book_id>")
def part_of_speech(book_id='all'):
    if book_id == '1' or book_id == '2' or book_id == '3' or book_id == '4':
        query = db.processed_text.find_one({'book_id': book_id})  #query if data present against the book_id
        if query:#if something come in the response
            if query["nouns"]:# if the response contains  nouns
                return  query['total_verbs_nouns'] + " " + query['nouns'] +"verbs :"+query["verbs"]  #the return the json of total nouns and verbs in the book and the nouns and the verbs
            else:#if the query is empty no document is present relative to the book id
                if query["stemmed_words_count"]:                # if the stemmed words and count is present but the noun  and verbs are not
                    stemmed_words_count = json.loads(query["stemmed_words_count"]) #just load the json into the dictionaries
                    stemmed_words = json.loads(query["stemmed_words"])#just load the json into the dictionaries
                    nouns, verbs = Task3.part_of_speech(stemmed_words,stemmed_words_count)  #trigger the function to find the nouns and verbs with the present stemmed words
                    total_noun_verbs = {'total_nouns': len(nouns), 'total_verbs': len(verbs)} #store the total nouns and total verbs in the seprate dictionary
                    updateQueryTask3(book_id, nouns, verbs, total_noun_verbs, stemmed_words, stemmed_words_count) #update the document which already present with respective val
                    return  json.dumps(total_noun_verbs) + json.dumps(nouns) +"verbs : "+json.dumps(verbs)  #return  the json of total nouns verbs, verbs and nouns

                else: # when document is present but it neither contains nouns and verbs and stemmed word count and stemmed words
                    stemmed_words_count, stemmed_words = Task2.stemming(book_id) #tringger the task2 function to get the stemmed words and stemmed words count
                    nouns, verbs = Task3.part_of_speech(stemmed_words,stemmed_words_count) #tringger the task3 function to get the nouns ,verbs
                    total_noun_verbs = {'total_nouns': len(nouns), 'total_verbs': len(verbs)} #dictionary of total noun and total verbs
                    updateQueryTask3(book_id, nouns, verbs, total_noun_verbs, stemmed_words, stemmed_words_count) #update the document with nouns,verbs,total noun verbs,stemmed words,stemmed words count
                    return   json.dumps(total_noun_verbs) + "nouns :"+json.dumps(nouns) +"verbs : "+json.dumps(verbs) #return the json total_noun_verbs and nouns and verbs
        else:      # when no document present agains book_id
            stemmed_words_count, stemmed_words = Task2.stemming(book_id)# trigger function to get the stemmed words and stemmed words count
            # task3
            nouns, verbs = Task3.part_of_speech(stemmed_words,stemmed_words_count) #trigger the function part of speech to get the nouns and verbs
            total_noun_verbs = {'total_nouns': len(nouns), 'total_verbs': len(verbs)} #total verbs and total verbs
            insetQueryTask3(book_id, nouns, verbs, total_noun_verbs, stemmed_words, stemmed_words_count) #insert and the data into the database

            return  json.dumps(total_noun_verbs) + "nouns:" + json.dumps(nouns)  +"verbs : "+json.dumps(verbs) #return the json of nouns and verbs and total verbs and total nouns
    elif book_id == 'all' or book_id == 'ALL':
        list_of_all_books = ['1', '2', '3', '4'] #list of all books
        my_dict_total_nv = {}# dictionary for total verbs and nouns
        my_dict_total_n = {} #dictionay for nouns in each book
        my_dict_total_v = {} #dictiony of  verbs in each book
        for book_no in list_of_all_books: #iterating through each book
            query = db.processed_text.find_one({'book_id': book_no}) #query if data present against the book_id
            if query:#if something come in the response
                if query["nouns"]:# if the response contains  nouns
                    nouns = json.loads(query["nouns"]) #load the nouns in the nouns dictionary
                    verbs = json.loads(query["verbs"])#load the verbs in the verbs dictionary
                    total_noun_verbs = json.loads(query['total_verbs_nouns']) #load the toatl nouns and berbs in the total_noun_verbs dictionary
                else: # when the stemmed words and count is present but the noun  and verbs are not
                    if query["stemmed_words_count"]:# if the stemmed words and count is present but the noun  and verbs are not
                        stemmed_words_count = json.loads(query["stemmed_words_count"])#just load the json into the dictionaries
                        stemmed_words = json.loads(query["stemmed_words"])#just load the json into the dictionaries
                        nouns, verbs = Task3.part_of_speech(stemmed_words,stemmed_words_count)#trigger the function to find the nouns and verbs with the present stemmed words
                        total_noun_verbs = {'total_nouns': len(nouns), 'total_verbs': len(verbs)}#store the total nouns and total verbs in the seprate dictionary
                        updateQueryTask3(book_no, nouns, verbs, total_noun_verbs, stemmed_words, stemmed_words_count)#update the document which already present with respective val

                    else:# when document is present but it neither contains nouns and verbs and stemmed word count and stemmed words
                        stemmed_words_count, stemmed_words = Task2.stemming(book_no)#tringger the task2 function to get the stemmed words and stemmed words count
                        nouns, verbs = Task3.part_of_speech(stemmed_words,stemmed_words_count)#tringger the task3 function to get the nouns ,verbs
                        total_noun_verbs = {'total_nouns': len(nouns), 'total_verbs': len(verbs)}#dictionary of total noun and total verbs
                        updateQueryTask3(book_no, nouns, verbs, total_noun_verbs, stemmed_words, stemmed_words_count)#update the document with nouns,verbs,total noun verbs,stemmed words,stemmed words count

            else:   # when no document present agains book_id

                stemmed_words_count, stemmed_words = Task2.stemming(book_no)# trigger function to get the stemmed words and stemmed words count
                # task3
                nouns, verbs = Task3.part_of_speech(stemmed_words,stemmed_words_count)#trigger the function part of speech to get the nouns and verbs
                total_noun_verbs = {'total_nouns': len(nouns), 'total_verbs': len(verbs)}#total verbs and total verbs
                insetQueryTask3(book_no, nouns, verbs, total_noun_verbs, stemmed_words, stemmed_words_count)#insert and the data into the database

            my_dict_total_nv = Counter(my_dict_total_nv) + Counter(total_noun_verbs)#total_nouns and verbs in the all books will come in this dictionary
            my_dict_total_n = Counter(my_dict_total_n) + Counter(nouns)#total nouns of all books dictionary
            my_dict_total_v = Counter(my_dict_total_v) + Counter(verbs)#total verbs pf all books dictionary

        return json.dumps(my_dict_total_nv) + "nouns :" + json.dumps(my_dict_total_n) + " verbs " + json.dumps(my_dict_total_v) #return the json of total nouns ,verbs and total verbs nouns
    return "task 3 Books only from 1 to 4"


@app.route("/similar_documents/<first_book>/<second_book>", methods=['GET'])
def similar_document(first_book, second_book):

    if first_book== '1' or first_book == '2' or first_book == '3' or first_book == '4' :
        if second_book== '1' or second_book == '2' or second_book == '3' or second_book== '4':
             percentage = Task4.sentence_similarity(first_book, second_book)#trigger the function sentence similarity that will return the score of similarity between two books
             return "The similarity between the two documents is =" + str(percentage) + " percent" #return the score of similarity between two books

    return "Books only from 1 to 4"

@app.route("/send_a_word/<book_id>/<word>")
def send_a_word(book_id, word):
    if book_id == '1' or book_id == '2' or book_id == '3' or book_id == '4' :

        stemmer = SnowballStemmer('english') #intializing the stemmer
        base_word = stemmer.stem(word) #stem the word that is comming
        query = db.processed_text.find_one({'book_id': book_id}) #query if data present against the book_id

        if query:#if something come in the response
            if query["stemmed_words_count"]:  # if stemmed_words_count dictionary is present in database
                stemmed_words_count = json.loads(query["stemmed_words_count"]) #load the json of stemmed_words in the stemmed_words_count variable
                return  base_word + ":" + str(stemmed_words_count.get(base_word,"Word not exists"))#return the stemmed_word with its count
            else:  # if words_count is not present ,id database crashes so not create the collection again just update it
                stemmed_words_count, stemmed_words = Task2.stemming()  # calling function written in main.py to calculate the word_count with respect to book_id
                updateQueryTask2(book_id, stemmed_words,
                                 stemmed_words_count)  # updating words against book_id in the database so that next time no need to call the main function again
                return  base_word + ":" + str(stemmed_words_count.get(base_word,"Word not exists"))#return the stemmed_word with its count
        else:#if the query is empty no document is present relative to the book id
            stemmed_words_count, stemmed_words = Task2.stemming()#trigger the function in the task2 to get the stemmed words and stemmed words count
            insetQueryTask2(book_id, stemmed_words, stemmed_words_count)#inset the document in the database
            return  base_word + ":" + str(stemmed_words_count.get(base_word,"Word not exists")) #return the stemmed_word with its count

    return "Books only from 1 to 4"

@app.route("/similarity_of_all/")
@app.route("/similarity_of_all/<string>")


def similarity_of_all(string='all'):
    if string.lower() == 'all':
        list_of_sim_matrix = dict() #creating a dictionary for the similarities score
        count = 1 #intializing count with 1 which having index of book 1
        while (count <= 4):#iterate through all 4 books
            count_for_second_book = 4 #sceond count has second book indexes
            while (count_for_second_book >= 1): #conditions for books remain in the limit
                percentage_of_each = Task4.sentence_similarity(str(count), str(count_for_second_book))#triggering task 4 function to get the similarity between two book at a ttime
                list_of_sim_matrix[str(count) + ' and ' + str(count_for_second_book)] = str(percentage_of_each)
                count_for_second_book -= 1 #decreement book second

            count += 1 #increement book first
        return json.dumps(list_of_sim_matrix)
    return "Not a required String"


def insertQueryTask1(book_id, data):
    var = db.processed_text.insert(
        {
            "book_id": book_id,
            "words": json.dumps(data),
            "stemmed_words": '',
            "stemmed_words_count": '',
            "nouns": '',
            "verbs": '',
            "total_verbs_nouns": ''
        })



def insetQueryTask2(book_id, stemmed_data, stemmed_words_count):
    var = db.processed_text.insert(
        {
            "book_id": book_id,
            "words": '',
            "nouns": '',
            "verbs": '',
            "total_verbs_nouns": '',
            "stemmed_words": json.dumps(stemmed_data),
            "stemmed_words_count": json.dumps(stemmed_words_count)

        }
    )


def insetQueryTask3(book_id, nouns, verbs, total_verbs_nouns, stemmed_words, stemmed_words_count):
    var = db.processed_text.insert(
        {
            "book_id": book_id,
            "words": '',
            "nouns": json.dumps(nouns),
            "verbs": json.dumps(verbs),
            "total_verbs_nouns": json.dumps(total_verbs_nouns),
            "stemmed_words": json.dumps(stemmed_words),
            "stemmed_words_count": json.dumps(stemmed_words_count)

        }
    )


def updateQueryTask1(book_id, data):
    db.processed_text.update(
        {"book_id": book_id},
        {
            "$set": {"words": json.dumps(data)}
        }, upsert=False, manipulate=True, multi=True, check_keys=True)


def updateQueryTask2(book_id, stemmed_words, stemmed_words_count):
    var = db.processed_text.update(
        {"book_id": book_id},
        {
            "$set": {"stemmed_words": json.dumps(stemmed_words),
                     "stemmed_words_count": json.dumps(stemmed_words_count)

                     },
        }, upsert=False, manipulate=True, multi=True, check_keys=True

    )


def updateQueryTask3(book_id, nouns, verbs, total_verbs_nouns, stemmed_words, stemmed_words_count):
    var = db.processed_text.update(
        {"book_id": book_id},

        {"$set": {"nouns": json.dumps(nouns),
                  "verbs": json.dumps(verbs),
                  "stemmed_words": json.dumps(stemmed_words),
                  "stemmed_words_count": json.dumps(stemmed_words_count),
                  "total_verbs_nouns": json.dumps(total_verbs_nouns)
                  }},
        upsert=False, manipulate=True, multi=True, check_keys=True)


if __name__ == "__main__":
    app.run(debug=True)
