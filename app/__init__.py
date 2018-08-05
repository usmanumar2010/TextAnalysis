from flask import Flask
from pymongo import MongoClient


client = MongoClient('localhost:27017') # Mongo Client created
db = client.hell # connectavo is database name

app = Flask(__name__)



@app.route("/")
def index():
    
    return "hello world"

@app.route("/for_insertion/")
def for_insertion():
    var = db.oye.insert_one(
        {
            "book_id": '1',
            "words": 'usman',
            "dude":'sucks'
        }
    ).inserted_id

    print(var)    
    return "hi"



@app.route("/for_update/<book_id>")
def for_update(book_id):
    var = db.oye.update(
        {"book_id":book_id},
        {
            "$set":{"words": "hell","dude":"fuck"}
        }

    )
    return "hi"




if __name__ == "__main__":
    app.run(debug=True)
