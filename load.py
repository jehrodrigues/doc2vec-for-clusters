import gensim
import os
import re
import six
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from gensim.models.doc2vec import TaggedDocument
from models import Record
 
def get_doc_list(folder_name):
    corpus = []
    cursor = Record().get_knowledgebases()
    for row in cursor.fetchall():
        line = row[0] + ' ' + row[1]
        corpus.append(line)
    return corpus
 
def get_doc(folder_name):
 
    doc_list = get_doc_list(folder_name)
    tokenizer = RegexpTokenizer(r'\w+')
    #en_stop = get_stop_words('en')
    #p_stemmer = PorterStemmer()
    p_stemmer = RSLPStemmer()
 
    taggeddoc = []
 
    texts = []
    for index,i in enumerate(doc_list):
        # for tagged doc
        wordslist = []
        tagslist = []
 
        # clean and tokenize document string
        raw = gensim.utils.to_unicode(i, 'latin1').lower()
        print index,' - ',raw,'\n'
        tokens = tokenizer.tokenize(raw)
        #print tokens
 
        # remove stop words from tokens
        #stopped_tokens = [i for i in tokens if not i in en_stop]

        #Remove StopWords
        stopped_tokens = [word for word in tokens if word not in stopwords.words('portuguese')]
        #print stopped_tokens
 
        # remove numbers
        number_tokens = [re.sub(r'[\d]', ' ', i) for i in stopped_tokens]
        number_tokens = ' '.join(number_tokens).split()
        #print number_tokens,'\n'
 
        # stem tokens
        #stemmed_tokens = [p_stemmer.stem(i) for i in number_tokens]

        #Stemming
        stemmed_tokens = [p_stemmer.stem(i) for i in number_tokens]
        print stemmed_tokens,'\n'

        # remove empty
        length_tokens = [i for i in stemmed_tokens if len(i) > 1]
        # add tokens to list
        texts.append(length_tokens)
 
        #td = TaggedDocument(gensim.utils.to_unicode(str.encode(' '.join(stemmed_tokens))).split(),str(index))
        td = TaggedDocument(forward_transformer(stemmed_tokens), str(index))
        taggeddoc.append(td)

 
    return taggeddoc

def forward_transformer(tokens):
    return tokens