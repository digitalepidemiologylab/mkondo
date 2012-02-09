import string
import unicodedata

#Standard stop words as defined by Lucene. 
LUCENE_STOPWORDS = ["a", "and", "are", "as", "at", "be", "but", "by",  "for",
"if", "in", "into", "is", "it", "no", "not", "of", "on", "or", "s", "such",
"t", "that", "the", "their", "then", "there", "these", "they", "this", "to",
"was", "will", "with"]

STOPWORDS = LUCENE_STOPWORDS
STOPWORDS.remove('not')
STOPWORDS.remove('no')

def remove_punctuation_no_exclaim(punctuated):
	''' Removes all punctuation except for exclamation marks'''
	return punctuated.translate(string.maketrans("",""), string.punctuation.replace("!", ""))

def remove_punctuation(punctuated):
	''' Removes all punctuation.'''
	return punctuated.translate(string.maketrans("",""), string.punctuation)

def unicode2utf8(text):
	""" Convert a string from unicode to utf-8. """
	return unicodedata.normalize('NFKD', text).encode('utf-8', 'ignore') 	

def bag_no_stopwords(text, stopwords=LUCENE_STOPWORDS):
	""" Take a string, make it a bag of words, and remove specified stop_words"""
	bag_of_words = text.split()
	pruned = [w for w in bag_of_words if w not in stopwords]
	return pruned
