# ConnectavoAssignment

This repository demonstrates the use of Natural Language Processing operations with the help of python based API's.

Operations that are performed here are :

1.Word Processing

2.Stemmed/Lemmatized Word Count

3.Part of Speech Count

4.Document Similarity


## Prerequisites

* Python 3.5+
* MongoDB 3+
* virtualenv -- `pip install virtualenv`
* Flask --  `pip install flask`
* PyMongo -- `pip install pymongo`
* NLTK --  `pip install -U nltk`
* Gensim — `pip install -U gensim`

## Installatoin

* Clone the Repository
* Run a mongo server with `mongod` in command Prompt
* cd ConnectavoAssignment/flask/Scripts
* Write `activate flask` in Command Prompt in the above mentioned folder
* cd ../../  `You are in the main ConnectavoAssignment folder now`
* Run DatabaseConnection.py with  `pyhton DatabaseConnection.py`
* When the Server Start Running
* Write the following link in the tab [http://127.0.0.1:5000/] 

## Download

I have used the standard stop words that are present in nltk for that write  **`nltk.download('stopwords')`**


## Task 1
#### Word Processing
   
   I have used the standard stop words in this task with nltk.download('stopwords').This Api will return the refined book without stop      words .
   
* Routes 
    
     <http://127.0.0.1:5000/refined_book/>    for  viewing all refined books
    
     <http://127.0.0.1:5000/refined_book/1>   for viewing any specfic refined book <book_id> within 1 to 4

     <http://127.0.0.1:5000/refined_book/all> for viewing all refined books with a key word 'all'
     
* Params

     <http://127.0.0.1:5000/refined_book/book_id>
      
     book_id : Optional  Or book_id : ALL , 1 , 2 ,3 , 4
     
 
 
* Response

     json reponse of words list
      
     {key :value}  example {"the":"the" ,"book":"book"} 
      
      
## Task 2
#### Stemmed / Lemmatized Word Count

  I have used Snowball Stemmer in this task it is the latest Stemmer with many supportive languages and it is more advance then the       porter Stemmer. Quoting [Quora here](https://www.quora.com/What-is-the-most-popular-stemming-algorithms-in-Text-Classification)         ,Snowball is obviously more advanced in comparison with Porter and, when used, gives considerably more reliable results.

* Routes

    <http://127.0.0.1:5000/stemmed_lemmatized/>  when you want to stemmed all books at a time
    
    <http://127.0.0.1:5000/stemmed_lemmatized/1> when you want to stemmed book id within 1 to 4
    
    <http://127.0.0.1:5000/stemmed_lemmatized/all> when you want to stemmed all books at a time with a word all
    
* Params

     <http://127.0.0.1:5000/stemmed_lemmatized/book_id>
      
     book_id : Optional  Or book_id : ALL , 1 , 2 ,3 , 4    
    
* Response
      
      json response of words with there respective occurances
      
      {key:value)  example {"the": 50677, "project": 343}
 
  * **Task 2 Part b**  
  
       User can send a base word or a lemma of the base word (Ex: go or going) and ,is served the count of the particular query in          return    .   
       
  * Routes
  
        <http://127.0.0.1:5000/send_a_word/1/going>  when you want to find no of times stemmed word occurs in the documents 
        
  * Params

     <http://127.0.0.1:5000/send_a_word/book_id/word>
      
     book_id  : 1 , 2 ,3 , 4       
     word : Any word can be the param
     
   * Response
          
        In response you will get the json response
              
              {key:value} or {"word":"count"} example: {go:126}
 
 ## Task 3
 #### Parts of Speech (PoS) Count
 
   I have used nltk for gathering the part of speech in the book ,nltk.pos_tag(tokens) this function of nltk tagged each tokken or word    with the respective part of speech.
   
 * Routes
   
      <http://127.0.0.1:5000/part_of_speech/>  when you want the part of speech of all the books combined
      
      <http://127.0.0.1:5000/part_of_speech/1> when you want the part of speech specified book id within 1 to 4
      
      <http://127.0.0.1:5000/part_of_speech/all> when you want the part of speech  of all the books combined specified by all
      
      
   * Params

     <http://127.0.0.1:5000/part_of_speech/book_id>
      
     book_id  :Optional  or book_id:ALL, 1 , 2 ,3 , 4       
      
   
 * Response
           
    json response of verbs and nouns and total verbs in the book and total nouns in the book
           
    {key: value}{key:value}{key:value} or {"total_nouns":"count","total_verbs":"count"}{"word_noun":"count:}{"word_count":"count"}
         
     example :{"total_nouns": 11909, "total_verbs": 49} {"'the": 97, "'project": 4, "}
         
 
  ## Task 4
  #### Document Similarity / Difference
     
   I have used Gensim in this task because Gensim is so fast,Gensim processes data in a streaming fashion with Memory 
   independence,Efficient Implementations .It is a very well optimized, but also highly specialized, library for doing jobs in the
   periphery of "WORD2VEC". That is: it offers an easy, surpringly well working and swift AI-approach to unstructured raw texts, based 
   on a shallow neural network. If you are interested in prodution, or in getting deeper insights into neural networks, you might also 
   have a look on TensorFlow, which offers a mathematically more generalized model, yet to be paid by some ‘unpolished’ performance    
   and scalability issues by now. Reference this [Why Gensim](https://www.quora.com/When-is-better-to-use-NLTK-vs-Sklearn-vs-Gensim) 
   and [Why Fast Approach](https://www.quora.com/What-makes-Gensim-so-fast) 
    
   * Routes
      <http://127.0.0.1:5000/similar_documents/1/1>  When you want to check the similarity between two books book id within 1 to 4
   
   * Params

     <http://127.0.0.1:5000/similar_documents/book_id/book_id>
      
     book_id  : 1 , 2 ,3 , 4       
    
   * Response
          
      In response we get the percentage score of the similarity
          
      Example: The similarity between the two documents is =80.87093602105139 percent
          
          
  * **Task 4 Part b**  
  
       User can send a query for all documents and is returned comprehensive results of all possible pairs of documents compared to each   other.
       
   * Routes
   
      <http://127.0.0.1:5000/similarity_of_all/>    you can call this api without specifying anything
      
      <http://127.0.0.1:5000/similarity_of_all/all>  when you want to compare each book with any other book 
      
   * Params

     <http://127.0.0.1:5000/similarity_of_all/book_id/>
      
     book_id  : Optional  or book_id : all
   
   
   * Response
          
     In response we get the percentage score of the similarity of all the books with each other   
     
     1 and 1 =80.87093602105139 percent
     
     similarly 1 and 2,1 and 3, 1 and 4 , 2 and 1, 2 and 2, 2 and 3 ,2 and 4, 3 and 1, 3 and 2,3 and 3 , 3 and 4 ,4 and 1, 4 and 2  
    
   ,4 and 3 and 4 and 4
          
        
     
           
