import json
import sys

from flask import Flask
from pymongo import MongoClient
sys.path.append("./Questions/")
import Task2
import Task1
import Task3
import  Task4
# sys.path.append("/Questions/Task1.py")

app = Flask(__name__)

# configration ,instantiate database connection object
client = MongoClient('localhost', 27017)



db = client.text_analysis


# default routing provies reference to all routes


@app.route("/")
def hello():
    return "Hello Connectavo"


@app.route("/refined_book/<book_id>")
def refined_book(book_id):
    if book_id == '1' or book_id == '2' or book_id == '3' or book_id == '4':
        query = db.processed_text.find_one({'book_id': book_id})
        if query:
            if query["words"]:  # if words_count dictionary is present in database
                words_json = query["words"]
                # words_dictionary = json.loads(words_json)  # converting json to a dictionary
                return "direct"+words_json
            else:  # if words_count is not present ,id database crashes so not create the collection again just update it
                data = Task1.show_the_list_of_stop_words()  # calling function written in main.py to calculate the word_count with respect to book_id
                updateQueryTask2(book_id,
                                 data)  # updating words against book_id in the database so that next time no need to call the main function again
                return "updated"+json.dumps(data)
        else:
            words_are = Task1.show_the_list_of_stop_words()
            insertQueryTask1(book_id, words_are)
            return "HELLO" + json.dumps(words_are)
    return "Books only from 1 to 4"


@app.route("/stemmed_lemmatized/<book_id>")
def stemmed_lemmatized(book_id):

    if book_id == '1' or book_id == '2' or book_id == '3' or book_id == '4':
        query = db.processed_text.find_one({'book_id': book_id})
        print("-----------------")
        print(query)
        print("-----------------")
        if query:
            if query["stemmed_words_count"]:  # if stemmed_words_count dictionary is present in database
                stemmed_words_count = query["stemmed_words_count"]
                # words_dictionary = json.loads(words_json)  # converting json to a dictionary
                return "direct"+stemmed_words_count
            else:  # if words_count is not present ,id database crashes so not create the collection again just update it
                stemmed_words_count,stemmed_words = Task2.stemming()  # calling function written in main.py to calculate the word_count with respect to book_id
                updateQueryTask2(book_id,stemmed_words, stemmed_words_count)  # updating words against book_id in the database so that next time no need to call the main function again
                return "updated"+json.dumps(stemmed_words_count)
        else:
            stemmed_words_count, stemmed_words = Task2.stemming()
            insetQueryTask2(book_id, stemmed_words, stemmed_words_count)
            return "HELLO" + json.dumps(stemmed_words_count)
    return "Books only from 1 to 4"


@app.route("/part_of_speech/<book_id>")
def part_of_speech(book_id):
    if book_id == '1' or book_id == '2' or book_id == '3' or book_id == '4':
        query = db.processed_text.find_one({'book_id': book_id})
        if query:
            if query["nouns"]:
                return "direct"+query['total_verbs_nouns']+" "+query['nouns']
            else:
                stemmed_words_count, stemmed_words = Task2.stemming()
                nouns, verbs = Task3.part_of_speech(stemmed_words)
                total_noun_verbs = {'total_nouns': len(nouns), 'total_verbs': len(verbs)}

                updateQueryTask3(book_id, nouns, verbs, total_noun_verbs, stemmed_words, stemmed_words_count)
                return "task 3 updated" + json.dumps(total_noun_verbs) + json.dumps(nouns)


        else:
            stemmed_words_count, stemmed_words = Task2.stemming()
            #insetQueryTask2(book_id, stemmed_words, stemmed_words_count)

            #task3
            nouns, verbs = Task3.part_of_speech(stemmed_words)
            total_noun_verbs = {'total_nouns': len(nouns), 'total_verbs': len(verbs)}
            insetQueryTask3(book_id, nouns, verbs, total_noun_verbs,stemmed_words,stemmed_words_count)

            return "HELLO" +json.dumps(total_noun_verbs)+" "+json.dumps(nouns)+ json.dumps(nouns)
    return "task 3 Books only from 1 to 4"



def insertQueryTask1(book_id, data):
        var = db.processed_text.insert(
            {
                "book_id": book_id,
                "words": json.dumps(data),
                "stemmed_words": '',
                "stemmed_words_count":'',
                "nouns":'',
                "verbs":'',
                "total_verbs_nouns":''
            })
        if var:
            print("nice")


def insetQueryTask2(book_id, stemmed_data, stemmed_words_count):
        var=db.processed_text.insert(
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


def insetQueryTask3(book_id,nouns, verbs,total_verbs_nouns,stemmed_words,stemmed_words_count):
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

    return "updated" + json.dumps(total_verbs_nouns) + " " + json.dumps(nouns)


def updateQueryTask1(book_id, data):
    db.processed_text.update(
        {"book_id": book_id},
        {
            "$set":{"words": json.dumps(data)}
        } ,upsert=False, manipulate=True, multi=True, check_keys=True  )


def updateQueryTask2(book_id, stemmed_words, stemmed_words_count):


    var=db.processed_text.update(
        {"book_id": book_id},
        {
            "$set":{"stemmed_words": json.dumps(stemmed_words),
                    "stemmed_words_count": json.dumps(stemmed_words_count)

                    },
        },upsert=False, manipulate=True, multi=True, check_keys=True

    )



def updateQueryTask3(book_id,nouns,verbs,total_verbs_nouns, stemmed_words, stemmed_words_count):


    var=db.processed_text.update(
        {"book_id": book_id},

        {"$set":{"nouns": json.dumps(nouns),
                    "verbs": json.dumps(verbs),
                    "stemmed_words": json.dumps(stemmed_words),
                    "stemmed_words_count": json.dumps(stemmed_words_count),
                    "total_verbs_nouns": json.dumps(total_verbs_nouns)
                    }},
                    upsert = False, manipulate = True, multi = True, check_keys = True)
    if var:
        print(var)

@app.route("/similar_documents/<book_id>/<your_string>",methods=['GET'])
def similar_document(book_id,your_string):

    similar= Task4.sentence_similarity(book_id+".txt",your_string)
    print("returning data")
    return str(round(similar, 1))

if __name__ == "__main__":
    app.run(debug = True)
