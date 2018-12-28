# Tweet-Classification
A simple Naive Bayes classification of tweets into locations
# Input Files
We had 2 input files
a) tweets_train.txt
b) tweets_test1.txt
 The two files contain the tweets followed by the location of tweet.
 The aim was to implement a simple Naive Bayes classifier to correctly classifiy these tweets into a total of 12 locations.
 
# Naive Bayes assumptions
We used a bag of words model for this implementation. We used the words from the training text tweets to train the Naive Bayes Model. However, we assumed that the test tweets will also have words from the same set as that of the training set. If a completely new word appears during the testing cycle we assign it a very low probability.
We also assumed the independence between any two words appearing in the tweet. For example, word 'He' and word 'ran' are independent of eachother given a location. 

# Design Decisions
After reading the text input file we are parsing the data based on a regular expression (.,_[A-Z]{2}|.,_Ontario) this regex will extract every location and the tweet associated with it. We are removing the blankspaces,non numeric,non alphabetical characters from the data. We are also converting the text into lower case for equivalence. For eg Box is same as box. We have not removed the stopwords. Hence you can see these stopwords in most frequent list. We have not calculated probabilities based on symbols like # or @.

# Implementation
We begin by seperating words of each tweet and append the same to a dictionary, containing {"Location" : {"Bag of words" : "Frequency of appearance of respective word"}}

We then calculate total number of words associated with each location. Let's assume, for location 1 - we have 10 words & location 2 - 20 words. Out of the 10 words in location 1, let's assume the frequency of appearance of the words "hello" is 3 & that of "hi" is 4. So the conditional probability of the appearance of word "hello" given the location is 1 = 3/10 and so on. We call this term - "P(word|location)" denoted by the variable - 'location[city][word]'

We then calculate the prior which is the ratio of the total number of tweets made at 1 specific location to the sum of total number of tweets at all the locations. We call this the "prior" denoted by the variable - 'prior' and calculate it's probability in the function 'prior_calculation'.

Having found P(word|location) and the prior, we multiply these 2 terms to find the overall probability of a word appearing at a specific location denoted by 'final_prob' and this value is called for the prediction of location by the 'predict_product' function. While determining the appearance of a word at a location where it has never appeared earlier, we assign it a significantly low probability of 1/(2*total_word_count), since, we can neither assign it a 0 (would make the entire product 0) or a 1 (signifies that the word appears in every tweet at that location).

Now that we are set with our model, we finally begin reading the test set and seperating the tweets and their locations. We now test these tweets on our model and write the output to another text file. We also calculate the accuracy of our model by calculating the number of times we have predicted the location right with respect to a tweet to the total number of tweets and multiply the same with 100.

# Accuracy
The accuracy of our model trained on the given training set when executed on the given testing set is 66.6%.
