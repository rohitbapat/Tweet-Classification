#!/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 09:11:42 2018

@author: rohit akshay
"""
import re
import heapq
import sys

# Seperates out the entire tweet from the location
def tweet_synthesis(tweet_message,lower_case=True):
    if lower_case:
        tweet_message=tweet_message.lower()
    #split tweet to get words
    tweet_words=tweet_message.split()
    return tweet_words

# Forms dictionary of location - bag of words - frequency of each word
def form_dictionary(place,tweet):
    global total_tweets
    total_tweets+=1
    if place in location.keys():
        tweet_count[place]+=1
    else:
        tweet_count[place]=1
    for tweet_word in tweet_synthesis(tweet):
        if place in location.keys():
            if tweet_word in location[place].keys():
                location[place][tweet_word]+=1
            else:
                location[place][tweet_word]=1
        else:
            word_list={}
            word_list[tweet_word]=1
            location[place]=word_list
            word_list={}

# Calculate prior - Number of tweets at one location/Total number of tweets
def prior_calculation():
    for city in location.keys():
        # prior is tweet count for a location divided by total tweets
        priors[city]=float(tweet_count[city]/total_tweets)

# function where we calculate the likelihoods of word given a location based on count 
def calc_condProb(city,total_count):
    for word in location[city].keys():
        # calculate probability for a word given a location
        location[city][word]=(location[city][word])/total_count
       
# precompute the likelihood for each location and the set of words it has
def precompute():
    for city in location.keys():
        total_count=0
        total_count=sum(location[city].values())
        global total_word_count
        total_word_count+=total_count
        calc_condProb(city,total_count)
        
# predict probability based on single line tweet input and probability scores for each value
def predict_product(city,predict_tweet):
    product=1
    for word in predict_tweet:
        if(location[city].get(word)!=None):
            likelihood_prob=location[city][word]
        else:
            # factor of 2*total_word_count taken for missing words
            likelihood_prob=1/(2*total_word_count)
        product=product*likelihood_prob
    return product

# function for calclating final product of likelihoods and product
def predict_tweet_function(new_tweet):          
    predict_tweet=tweet_synthesis(new_tweet)
    final_prob={}
    for city in location.keys():
        prob_cal=predict_product(city,predict_tweet)
        prob_cal=prob_cal*priors[city]
        final_prob[city]=prob_cal
    max_value=max(final_prob.values())
    for city,value in final_prob.items():
        if(value==max_value):
            return city

# function to calculate top 5 words used in tweet for each loaction
# https://stackoverflow.com/questions/7197315/5-maximum-values-in-a-python-dictionary            
def find_top(city,word_freq):
    B=heapq.nlargest(5,word_freq,key=word_freq.get)
    print(city,end=' ')
    for C in B:
        print(" ",C,end=' ')
    print("\n")

#function to read the test file for the testing tweets        
def readtestFile():  
    count=0   
    total_count=0
    test_content=""
    f1=open(testing_file,'r',errors='ignore')
    test_content=f1.read()
    f1.close()
    last_start=0
    last_loc=""
    len(last_loc)
    test_matches=re.finditer('(.*,_[A-Z]{2}|.*,_Ontario)',test_content)
    for match in test_matches:
        total_count+=1
        if(match.start()!=0):
            tweet=test_content[last_start+len(last_loc)+1:match.start()]
            original_tweet=tweet
        # place to store the output file
        fileopen=output_file
        fwrite=open(fileopen,"a")
        if(match.start()!=0):
            tweet=re.sub(r'[^\w\s\d]','',tweet)
            max_city=predict_tweet_function(tweet)
            if max_city==last_loc:
                 count+=1
            fwrite.write(''.join((max_city," ",last_loc," ",original_tweet)))    
        last_start=match.start()
        last_loc=match.group()
        last_loc=last_loc.replace(" ","")
    fwrite.close()
    # calculation of accuracy
    (count/total_count)*100

# initialization of dictionaries
tweet_count={}
total_tweets=0
total_word_count=0
location={}
word_list={}
priors={}

training_file=str(sys.argv[1])
testing_file=str(sys.argv[2])
output_file=str(sys.argv[3])

# fetching of tweets and locations discussed with Swarnima(shsowani)
f=open(training_file,'r',errors='ignore')
content=f.read()
f.close()
matches=re.finditer('(.*,_[A-Z]{2}|.*,_Ontario)',content)
last_start=0
last_loc=0
for match in matches:
    if(match.start()!=0):
        tweet=content[last_start+len(last_loc)+1:match.start()]
    if(match.start()!=0):
        tweet=re.sub(r'[^A-Za-z\s\d]','',tweet)
        form_dictionary(last_loc,tweet)
    last_start=match.start()
    last_end=match.end()
    last_loc=match.group()
    last_loc=last_loc.replace(" ","")

# initialization of dictionaries for priors and precompute call
prior_calculation()
cond_prob={}
word_list={}
total_count=0
precompute()
readtestFile()
for city in location.keys():
    word_freq=location[city]
    find_top(city,word_freq)