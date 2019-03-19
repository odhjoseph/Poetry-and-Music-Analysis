from nltk.stem.wordnet import WordNetLemmatizer
from collections import deque, defaultdict, Counter
from itertools import islice, combinations
from nltk.util import ngrams
from regex import sub
from nltk import data
from os import path, remove
import sys, codecs, operator
import os


def read_file(file_path):
	'''Read in a file object and return an opened representation of that file'''
	with codecs.open(file_path,'r','utf-8') as f:
		file_contents = "".join( f.read())
	f.close()
	return file_contents
def create_stopwords():
	'''Generate stopword list compiled by Ted Underwood'''
	with codecs.open(cwd + "text_cleaning_resources/underwood_stopwords.txt","r","utf-8") as stopwords_in:		
		stopwords = set(stopwords_in.read().split())
		return stopwords
def create_ortho_dict():
	'''Create mapping from spelling variant to controlled representation (orthographically-normalized representation) of word'''
	ortho_dict = {}
	with codecs.open(cwd + "text_cleaning_resources/orthographic_variants.txt","r","utf-8") as ortho:
		ortho = ortho.read().replace("\r","").lower().split("\n")[:-1]
		for row in ortho:
			sr = row.split("\t")
			ortho_dict[ sr[0] ] = sr[1]
	return ortho_dict
def standardize_spelling(w):
	'''Read in a word and return an orthograpically normalized representation of the word'''
	try:
		return ortho_dict[w]
	except:
		return w
def remove_stopwords(l):
	'''Read in a list of words and return that list sans stopwords'''
	return [w for w in l if w not in stopwords and len(w) > 1]
	
def remove_punctuation(s):
	'''Read in a string and return that strip without any punctuation except the hyphen and en-dash'''
	return sub("[^\P{P}']+0123456789", " ", s)

def lemmatize_word(w):
	'''Read in a single word and return it in its lemmatized state'''
	return lemmatizer.lemmatize(w)
def clean_sentence(s):
    s = remove_punctuation(s)
    words = s.split()
    for i in range(len(words)):    
        words[i] = standardize_spelling(words[i])
    return words
def bigramify(clean):
    bigrams = []
    for i in range(len(clean) - 1):
        bigrams.append((clean[i], clean[i +1]))
    return bigrams
def trigramify(clean):
    trigrams = []
    for i in range(len(clean) - 2):
        trigrams.append((clean[i], clean[i +1], clean[i + 2]))
    return trigrams
def ngramify(clean, n):
    ngrams = []
    for i in range(len(clean) - n + 1):
        grams = []
        for j in range(n):
            grams.append(clean[i + j])
        grams = tuple(grams)
        ngrams.append(grams)
    return ngrams
def check(bigram1, bigram2):
    if len(bigram1) == 0:
        return 0
    if len(bigram2) == 0:
        return 0
    count = 0
    match = 0
    for bi1 in bigram1:
        for bi2 in bigram2: 
            count += 1
            if bi1 == bi2: 
                match += 1
    return match/count * (len(bigram1) + len(bigram2))/ 2
def linesplit(file):
    lines = file.split('\n')
    if '' in lines:
        lines.remove('')
    return lines
def totalsimiliarity(file1, file2): 
    try: 
        poem1 = read_file(file1)
        poem2 = read_file(file2)
    except: 
        return False
    lines1 = linesplit(poem1)
    lines2 = linesplit(poem2)
    cleanlines1 = []
    for line in lines1:
        cleanlines1.append((clean_sentence(line), line))
    cleanlines2 = []
    for line in lines2:
        cleanlines2.append((clean_sentence(line), line))
    bigramlist1 = list()
    for line in cleanlines1:
        clean, l = line
        bigramlist1.append((trigramify(clean), l))
    bigramlist2 = list()
    for line in cleanlines2:
        clean, l = line
        bigramlist2.append((trigramify(clean), l))
    checklist = list()
    for gr1 in bigramlist1: 
        for gr2 in bigramlist2:
            g1, r1 = gr1
            g2, r2 = gr2
            checklist.append((check(g1, g2), r1, r2))
    t = 0
    c = 0
    for x in checklist: 
        i,j,k = x
        t += i
        c += 1
    return t/c


cwd = os.getcwd()
cwd += '/detect_reuse-master/'
stopwords = create_stopwords()
ortho_dict = create_ortho_dict()