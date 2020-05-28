#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 17:43:07 2020

@author: Charlie Zheng
"""
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer

#This class simulates the emails
class email():

    def __init__(self, id, fileName, score=0):
        #this is the id of the email
        self.id = id
        #read the file
        f = open(fileName,'rt')
        #make all words lowercase
        text = f.read()
        #split the text into words and strip all punctuation
        words = word_tokenize(text)
        #strip stop words and number, only remain the stems
        en_stopwords = stopwords.words('english')
        porter = PorterStemmer();
        self.words = [porter.stem(w) for w in words if w.isalpha() and not w in en_stopwords]
        #this is the score of its spamicity
        self.score = score

    def getId(self):
        return self.id

    def getWords(self):
        return self.words

    def getScore(self):
        return self.score

    def setScore(self, newScore):
        self.score = newScore

class filter():

    def __init__(self, threshold):
        # this is the threshold of the spam score
        self.threshold = threshold
        # the inbox stores all hams
        self.inbox = []
        # spams store all spams
        self.spams = []
        # the bag of words of spams
        self.spamBOW = {}
        # the bag of words of hams
        self.hamBOW = {}
    
    #this function determines the spamicity of each word
    def wordSpamicity(self, word):
        #the frequency of the word appeared in spams
        wordInSpam = 0
        #the frequency of the word appeared in hams
        wordInHam = 0
        #checking the bags of words to set the frequency
        if word in self.spamBOW.keys(): wordInSpam = self.spamBOW[word]
        if word in self.hamBOW.keys(): wordInHam = self.hamBOW[word]
        #calculating the probability of a spam word
        pws = float(wordInSpam/len(self.spams))
        pwh = float(wordInHam/len(self.inbox))
        if (pws + pwh) == 0: psw =0
        else: psw = float(pws/(pws+pwh))
        return psw
        
    #this function calcuates the spam score of the email according to its words' spamicity
    def spamScore(self,mail):
        score = 0;
        #getting the spamicity of each word
        for w in mail.getWords():
            spamicity = self.wordSpamicity(w)
            if spamicity > 0.9: score += 3
            if spamicity > 0.75 and spamicity <= 0.9: score += 2
            if spamicity > 0.5 and spamicity <= 0.75: score += 1
        return score
    
    #this function receives a new email, calculates its spam score, update the bags of words, and sort the email
    def receive(self, mail):
        score = self.spamScore(mail)
        mail.setScore(score)
        if score > self.threshold: 
            self.spams.append(mail)
            print(mail.getId() + ' is a spam. Its Spam score is ' + str(mail.getScore()))
            self.addWords(self.spamBOW, mail.getWords())
        else: 
            self.inbox.append(mail)
            print(mail.getId() + ' is not a spam. Its Spam score is ' + str(mail.getScore()))
            self.addWords(self.hamBOW, mail.getWords())
    
    #this function trains the filter
    def train(self, mail, isSpam):
        if isSpam is True: 
            self.spams.append(mail)
            self.addWords(self.spamBOW, mail.getWords())
        else: 
            self.inbox.append(mail)
            self.addWords(self.hamBOW, mail.getWords())
    
    @staticmethod
    def addWords(bow, words):
        checked = set()
        for w in words:
            if w not in checked: 
                checked.add(w)
                if w not in bow.keys(): bow.update({w:1})
                else: 
                    recur = bow[w] + 1
                    bow.update({w:recur})
            

#creating training and testing data
spam1 = email('spam1_train','spam1.txt')
spam2 = email('spam2_train','spam2.txt')
spam3 = email('spam3_test','spam3.txt')
ham1  = email('ham1_train','ham1.txt')
ham2  = email('ham2_train','ham2.txt')
ham3  = email('ham3_test','ham3.txt')
#creating the filter and set the threshold to 10
spamFilter = filter(10)
#training
spamFilter.train(spam1, True)
spamFilter.train(spam2, True)
spamFilter.train(ham1, False)
spamFilter.train(ham2, False)
#testing
spamFilter.receive(spam3)
spamFilter.receive(ham3)
