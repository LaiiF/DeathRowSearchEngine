# Death Row Last Statements Search Engine
Death Row last statements from inmates in Texas federal penitentiary. Search through their last words, find their statement classifications, and use the auto image captioner.


# Environment / How to Deploy
  Required packages: csv, re, nltk, time, operator, flask, flask_wtf, wtforms, flask_login, numpy, pandas, matplotlib, PIL(3.6), keras, tensorflow
  
  Langauge: Python 3.7, HTML
# To Run
*run on path: /.../Python/Sitch* 
 visit Western1499.pythonanywhere.com

# TFIDF Calculation
>Term Frequency(TF) * Inverse Document Frequency (IDF) = TF-IDF

>t = term (word)

>d = document (set of words)

>N = count of docs

>TF = count of t in d / num words in d

>DF = occurence of t in documents

>IDF = log(N/(DF +1))

>TF-IDF = TF * IDF

# Challenges
SEARCH:
>The first overall challenge I faced was sending information between Python and HTML. It is more natural to use a scripting language like JavaScript to work with HTML, so using Python took an extra process. To overcome it, I used request from flask to take input from HTML, then used render_template to send the data to HTML.

>The second challenge I faced was computing TFIDF. While our class was told we could use a library function to compute it, I did not take this route. Instead, I computed it myself using Shivagi Sareem's methodology (included in references below). After computing the TFIDF, I did the same for the query and ranked them in accordance to the highest TFIDF value and frequency of the word in the query. The result is limited to 10 documents.

CLASSIFIER:
>The challenges I ran into was converting the statement of strings into an array of values. To maximize value of certain words to gauge the best classification for them, I used the TFIDF values. Because they were already computed, they were helpful to give value to each word in the tokenized set of strings.

CAPTIONER:
>The challenges I ran into was building the model for the captioner. I could build the set of descriptions and images, but having the captioner truly understand the image and having enough training/testing data to truly give an accurate caption was difficult. To boot, pythonanywhere would not allow me to install keras or tensorflow due to a faulty disk quota exceeded error on 60% capacity.

OTHER CHALLENGES:
>During the semester, my personal Desktop and my laptop died. The motherboard of the desktop failed during use, and the master boot record of my laptop became corrupted. The only computer my family had left was a chromebook which I used up until the end of October. From there, we could afford a laptop for my mother which I used until the end of the semester. 
# Experiments
First experiment was to compute TFIDF each time without caching. The average time taken was: [50.11078429222107]s
With caching, the average time taken was: [0.04102754592895508]s

Second experiment was to search results without stopwords, stemming, or lemmatization. Without it, queries returned significantly less hits in documents. 

# Algorithms Search
>All algorithms stated are from file *search.py*
search(query)
>Receives an input *query* from user, tokenizes and stems the query, opens the csv document to read, creates the doclist = (index, TDCJNumber, FirstName, LastName, LastStatement) for each document. Then, counts the words in each Last Statement towards the totalwords variable. 
>Attempts to load TFIDF values of a specified document if it exists, else compute the TFIDF values. After computing, it is saved.
>Calls the ranking function to deliver a ranking based on TFIDF values and hit frequency within the user query.
>Then calls the output function to display the unparsed, unlemmatized, unstemmed document to the user.

output(ranking, doclist)
>Accepts a ranking and the original doclist and reshuffles the doclist into a display value in order of TFIDF values and query hit frequency.

rank(TFIDFvals, query_token, totaldocs, freqDictlist)
>Accepts the TFIDF value matrix, the tokenized query, the total number of docs, and a list of dictionaries of frequency to key.
>Ranks in accordance to TFIDF values and query hit frequency.

parseddoc(doclist)
>Accepts a list of all documents and parses it. Removes stop words, punctuation, lemmatizes, and stems the document. Returns a parsed list.

freqdict(parsedlist, freqDictlist)
>Accepts the parsedlist and the freqDictlist to append the freqDictlist of frequencies of words in docs.

get_doc(parsedlist)
>Generates info about the parsed doc list including the doc_id and the doc_length

TFCompute(freqDictlist, doc_info)
>Computes term frequency given the freqDictlist and the doc_info
>Returns the TF values

IDFCompute(freqDictlist, doc_info)
>Computes the Inverse Document Frequency given the freqDictlist and the doc_info
>Returns the IDF values

TFIDFCompute(TFvals, IDFvals)
>Accepts the TF values and the IDF values and computes TF * IDF
>Returns the TFIDF values for ranking.

saveTFIDF(TFIDFvals, name)
>Given the values to save and the name of the file to save it as, save the TFIDFvals as a pkl file

loadTFIDF(TFIDFvals, name)
>Given the empty TFIDF value matrix and the name of the pkl file to load, load the file contents into the variable TFIDFvals
>Now computation takes a fraction of the time

# Algorithms Classifier
classify():
>This function took in the document list from my dataset and sent it to the parsing function. After being parsed, the probability scores for each statement are computed. From there, the list along with the probability scores for each document are returned to HTML.

parselist(doclist):
>This function takes in the document list and parses each statement into tokens. Removing stopwords, providing lemmatization and stemming, and removing punctuation. 

findHits(parsedlist):
>Taking in the parsed list, this function computes the probability scores for each statement and returns the values. The dominant values are the classifications.

# Algorithms Captioner
captioner():
>This function openes the image file and loads it into memory. It creates the vocabulary using the captions, and trains captioner using this data. 

doclod(filename):
>Given the filename, this function pulls all the text from the captionlist and returns the textual output. 

takedesc(doc):
>This function maps the descriptions to the images themselves.

parsedesc(desc):
>Given the descriptions, this function parses through them and removes all stop words, punctuation, etc.

bagofwords(desc):
>Using the parsed desc list, this function creates the vocabulary to use for future captions.

savedesc(desc):
>Once the descriptions are mapped and made, they are saved to text so that these functions do not need to be called again.

loaddesc(desc):
>If the descriptions are already saved, load them without needing to recreate them.
# References
I have referenced two main sources for the coding of this search engine:
Shivagi Sareem at https://towardsdatascience.com/tfidf-for-piece-of-text-in-python-43feccaa74f8
Miguel Grinberg at https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

I have referenced one main source for the coding of the classifier:
InsightBot at http://www.insightsbot.com/bag-of-words-algorithm-in-python-introduction/

I have referenced one main source for the coding of the image captioner:
Harshall Lambda at https://towardsdatascience.com/image-captioning-with-keras-teaching-computers-to-describe-pictures-c88a46a311b8
To add from their portion, I've included a homepage, login page, caching, inverted index, lemmatization, and stemming.
  For the classifier, I streamlined the tokenization proccess and compiled the bag of words model based on all non-stop words in the last statements. 
  
