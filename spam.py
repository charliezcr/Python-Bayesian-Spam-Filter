#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 17:43:07 2020

@author: Charlie Zheng
"""
import nltk
nltk.download('punkt')
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer

class Email():
    """This class simulates the emails"""
    def __init__(self, id, file, score=0):
        self.id = id  # id of each email
        text = open(file,'rt').read()  # read the text of the file
        words = word_tokenize(text) # split the text into words and strip all punctuation

        # strip stop words and number, only remain the stems
        en_stopwords = stopwords.words('english')
        porter = PorterStemmer();
        self.words = [porter.stem(w.lower()) for w in words if w.isalpha() and not w in en_stopwords]

        self.score = score  # this is the score of the email's spamicity

    def get_id(self):
        return self.id

    def get_words(self):
        return self.words

    def get_score(self):
        return self.score

    def set_score(self, new_score):
        self.score = new_score


class Filter():
    """This class simulates the filter of the mailbox"""

    def __init__(self, threshold):
        """this is the threshold of the spam score"""
        self.threshold = threshold

        self.inbox = []  # the inbox stores all hams
        self.spams = []  # spams store all spams
        self.spam_bow = {} # the bag of words of spams
        self.ham_bow = {}  # the bag of words of hams


    def word_spamicity(self, word):
        """Determines the spamicity of each word.

        Args:
            word: the word to be calculated

        Returns:
            the spamicity of the word
        """
        word_spam = 0  # the frequency of the word appeared in spams
        word_ham = 0 # the frequency of the word appeared in hams

        #checking the bags of words to set the frequency
        if word in self.spam_bow.keys():
            word_spam = self.spam_bow[word]
        if word in self.ham_bow.keys():
            word_ham = self.ham_bow[word]

        #calculating the probability of a spam word
        pws = float(word_spam/len(self.spams))
        pwh = float(word_ham/len(self.inbox))
        if (pws + pwh) == 0:
            psw =0
        else:
            psw = float(pws/(pws+pwh))
        return psw


    def spam_score(self, mail):
        """Calcuates the spam score of the email according to its words' spamicity

        Args:
            mail: the mail to be calculated

        Returns:
            the spam score of the email according to its words' spamicity

        """
        score = 0

        #getting the spamicity of each word
        for w in mail.get_words():
            spamicity = self.word_spamicity(w)
            if spamicity >= 0.9:
                score += 3
            if spamicity >= 0.75 and spamicity < 0.9:
                score += 2
            if spamicity >= 0.5 and spamicity < 0.75:
                score += 1
        return score


    def receive(self, mail):
        """Receives a new email, calculates its spam score, update the bags of words, and sort the email

        Args:
            mail: the new mail to be received

        """

        # calculates the mail's spam score
        score = self.spam_score(mail)
        mail.set_score(score)

        # sort the mail and update the bags of words
        if score > self.threshold:
            self.spams.append(mail)
            print(mail.get_id() + ' is a spam. Its Spam score is ' + str(mail.get_score()))
            self.add_words(self.spam_bow, mail.get_words())
        else:
            self.inbox.append(mail)
            print(mail.get_id() + ' is not a spam. Its Spam score is ' + str(mail.get_score()))
            self.add_words(self.ham_bow, mail.get_words())


    def train(self, mail, is_spam):
        """Trains the filter

        Args:
            mail: the training mail
            is_spam: whether mail is spam or not
        """

        if is_spam:
            self.spams.append(mail)
            self.add_words(self.spam_bow, mail.get_words())
        else:
            self.inbox.append(mail)
            self.add_words(self.ham_bow, mail.get_words())


    @staticmethod
    def add_words(bow, words):
        """Adds words to the bag of words

        Args:
            bow: the bag of words
            words: the words to be added

        """
        checked = set()  # the checked words

        for w in words:
            checked.add(w)
            # update bag of words
            if w not in bow.keys():
                bow.update({w:1})
            else:
                recur = bow[w] + 1
                bow.update({w:recur})

if __name__ == "__main__":
    #creating training and testing data
    spam1 = Email('spam1_train','spam1.txt')
    spam2 = Email('spam2_train','spam2.txt')
    spam3 = Email('spam3_test','spam3.txt')
    ham1  = Email('ham1_train','ham1.txt')
    ham2  = Email('ham2_train','ham2.txt')
    ham3  = Email('ham3_test','ham3.txt')
    #creating the filter and set the threshold to 10
    spam_filter = Filter(10)
    #training
    spam_filter.train(spam1, True)
    spam_filter.train(spam2, True)
    spam_filter.train(ham1, False)
    spam_filter.train(ham2, False)
    #testing
    spam_filter.receive(spam3)
    spam_filter.receive(ham3)
