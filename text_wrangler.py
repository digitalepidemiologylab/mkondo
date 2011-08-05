import string

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
