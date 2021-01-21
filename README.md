# Python Bayesian Spam Filter
## Project Overview
 We receive a lot of mails but our mailbox automatically sorts the spams out and only take hams (the mail that you want, opposite of spams) in our inbox. How exactly does our mailbox calcualte whether the mail is a spam or not? This is a spam filter implemented in python to showcase the use of Naive Bayes Classifier and Bag-of-Words model in the our mail box.
## Contents
 For a detaile walk-through of the code and explanation of the theories, please look at [Python notebook](https://github.com/charliezcr/Python-Bayesian-Spam-Filter/blob/master/Spam_filter.ipynb) or [website](https://charliezcr.github.io/SpamFilter.html)<br>
 If you are more interested in the code itself, please read the [Python file](https://github.com/charliezcr/Python-Bayesian-Spam-Filter/blob/master/spam.py)<br>
 The rest txt files are training and testing data. <br>
## Modules
**pip install nltk**
- [nltk](https://www.nltk.org/): natural language processing
Please also download punctuation and stopwords in nltk
```
nltk.download('punkt')
nltk.download('stopwords')
```
