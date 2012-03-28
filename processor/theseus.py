#!/usr/bin/env python
# encoding: utf-8
"""
theseus.py
==========

A Python Library for text processing in The Observatorium project

Visit http://theobservatorium.eu/ for the latest version

.. rubric:: References
..  [Bun2006] Bun, K., & Ishizuka, M. (2006). Emerging topic tracking system in WWW. Knowledge-Based Systems, 19(3), 164-171. doi: 10.1016/j.knosys.2005.11.008.
..  [Ishzuka2001] Ishizuka, M. (n.d.). Topic extraction from news archive using TF*PDF  algorithm. Proceedings of the Third International Conference on Web Information Systems Engineering, 2002. WISE 2002., 73-82. IEEE Comput. Sci. doi: 10.1109/WISE.2002.1181645.
..  [Ishzuka2002] Ishizuka, M. (2001). Emerging Topic Tracking System. Proceedings Third International Workshop on Advanced Issues of E-Commerce and Web-Based Information Systems. WECWIS 2001, 2-11. IEEE Comput. Soc. doi: 10.1109/WECWIS.2001.933900

"""
from __future__ import division
import math
from stemming.porter2 import stem

class NotImplemented(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class DocNode:
    """
    The DocNode is the basic structue that olds each document in a corpus
    
        * *idn* Id number of the node
        * *fnm* File name of the Document
        * *txt* Text of the Document
        * *ttl* Time to Live
        * *lang='en'* The language of the text, defaults to english
    """

    def __init__(self, idn='', fnm='', txt='', ttl='', lang='en'):
        self.idn = idn
        self.fnm = fnm
        self.txt = txt
        self.ttl = ttl
        self.lang = lang
        self.sentences = []
        self.terms = []

    def extractSentences(self):
        """
        Extract all the sentences of the document
        """
        phraseSeparator = u".!?¡¿;:"
        breaker = u"+~&"

        #remove new lines and tabs
        temp1 = self.txt.replace("\t", " ")
        temp1 = temp1.replace("\r\n", " ")
        temp1 = temp1.replace("\n\r", " ")
        temp1 = temp1.replace("\n", " ")

        for el in phraseSeparator:
            temp1 = temp1.replace(el, el + breaker)

        temp1 = temp1.split(breaker)

        for stc in temp1:
            if len(stc.strip()) > 0:
                st1 = Sentence(stc.strip(), self.lang)
                st1.cleanText()
                self.terms.extend(st1.cleanedWords)
                self.sentences.append(st1)

    def stemDoc(self):
        """
        Stem the entire document by stemming each of the sentences in the document
        with a Porter Stemming algorithm (Note: English only)
        """
        if len(self.sentences) == 0:
            self.extractSentences()
        if len(self.sentences) > 0:
            for sentence in self.sentences:
                sentence.stemSentence()


class Sentence:
    """The Sentence is one of the building blocks of Documents"""

    def __init__(self, text, lang="en"):
        self.text = text
        self.language = lang
        self.cleaned = ""
        self.words = []
        self.cleanedWords = []
        self.stemedWords = []
        self.language = lang
        self._sscore = 0
        self._wscore = []

    def stemSentence(self):
        """
        Stem the sentence with the Porter Stemming algorithm
        """
        if len(self.cleanedWords) > 0:
            self.cleanText()
            for word in self.cleanedWords:
                stemed = stem(word.lower())
                if stemed not in self.stemedWords:
                    self.stemedWords.append(stemed)

    def cleanText(self):
        """
        Processes the raw text of a sentence:
            * creates a ``cleaned`` text without unauthorized letters,
            * creates a ``words`` list
            * creates a ``cleanedWords`` list without **stopwords**
        """
        self.cleaned = cleanStringNoDel(self.text)
        self.words = self.text.split()
        self.cleanedWords = []
        try:
            if self.language == "en":
                stop = enClean()
            elif self.language == "pt":
                stop = ptClean()
            elif self.language == "es":
                stop = esClean()
            elif self.language == "fr":
                stop = frClean()
        except:
            raise NotImplemented("Language not set! Use another Language")
        for word in self.cleaned.split():
            if word not in stop:
                self.cleanedWords.append(word)


class Domain:
    """
    A Domain is a field with a collection of words and a label

    Domain words should all be lower capital and without stopwords!
    """

    def __init__(self, label, words=[]):
        self.label = label
        self.words = words

    def addWord(self, word):
        if word not in self.words:
            self.words.append(word)

    def addWords(self, ws):
        for w in ws:
            self.addWord(w)

    def exportDomain(self):
        try:
            f = open(self.label + ".dom", 'w')
            for w in self.words:
                f.write(w + "\n")
            f.close()
        except:
            print "Couldn't export Domain " + self.label


class Channel:
    """
    A Channel contains all documents of a certain channel
    
        * *label* is a string
        * *doc* is a DocNode 
    """

    def __init__(self, label):
        self.label = label
        self.documents = []

    def addDocument(self, doc):
        self.documents.append(doc)


def jaccard(s1, s2):
    """
    Calculates de jaccard index for two lists
    """
    a1 = set(s1)
    a2 = set(s2)
    return (0.0 + len(a1.intersection(a2))) / len(a1.union(a2))


def extractPhrases(s1):
    """
    extractPhrases breaks a document into a sequence of phrases.

    XXX: We need to deal with numbers...
    """
    blocks = '.:;!?'
    for l in blocks:
        s1 = s1.replace(l, "|")
    s1 = s1.replace("||", "|")
    s1 = s1.replace("\r", "")
    s1 = s1.replace("\n\n", "|")
    return s1.split("|")


def cleanStringNoDel(s1):
    """
    Cleans strings from unauthorized letters
    """
    signs = u'\'\"\v\t\a\b\f\r/|\\!.-?¿¡:,_+"\n'
    letters = u'abcdefghijklmnopqrstuvwxyz áàéèíìóòúù äëïöü ãõñç'
    s1 = s1.lower()
    ot = u''
    for l in s1:
        if l in signs:
            ot += " "
        elif l in letters:
            ot += l
    ot2 = ot.split()
    ot = ''
    for w in ot2:
        ot += w + " "
    return ot[:-1]


def cleanString(s1):
    """
    Cleans strings from unauthorized letters
    """
    signs = u'!.-?¿¡:,_+"\n'
    letters = u'abcdefghijklmnopqrstuvwxyz áàéèíìóòúù äëïöü ãõñç'
    s1 = s1.lower()
    ot = u''
    for l in s1:
        if l in signs:
            ot += " "
        if l in letters:
            ot += l
    ot2 = ot.split()
    ot = ''
    for w in ot2:
        if (len(w) > 2) and (
        len(w) < 21): # Changed this to fit Cachopo2003 def.
            ot += w + " "
    return ot[:-1]


def dtf(token, corpus):
    """
    Calculates the fraction of documents of the corpus that have a token
    
        * *token* is a string               ex. 'word'
        * *corpus* is a ``list`` of ``lists``    ex. [['this' 'is' 'a' 'word' 'document']['document' 'two']]
    """
    out = 0.0
    for doc in corpus:
        if token in doc:
            out += 1.0
    return out / len(corpus)


def idf(token, corpus):
    """
    Calculates the inverse document frequency of a token
    
        * *token* is a string               ex. 'word'        
        * *corpus* is a ``list`` of ``lists``    ex. [['this' 'is' 'a' 'word' 'document']['document' 'two']]
    """
    return math.log((1.0 / dtf(token, corpus)), 2)  # Base 2 Logs?...


def tf(token, doc):
    """
    Calculates the term frequency in a certain document (doc)
    
        * *token* is a string   ex. 'word'
        * *doc* is a ``list``     ex. ['this' 'is' 'a' 'word' 'document']
    """
    return (0.0 + doc.count(token)) / len(doc)


def logtf(token, doc):
    """
    Calculates the Log Term Frequency in a certain document (doc)
    
        * *token* is a string   ex. 'word'
        * *doc* is a ``list``     ex. ['this' 'is' 'a' 'word' 'document']
    """
    return math.log(tf(token, doc))


def tfidf(token, doc, corpus):
    """
    Calculates the Term Frequency-Inverse Document Frequency of a token
    
        * *token* is a string               ex. 'word'
        * *doc* is a ``list``                 ex. ['this' 'is' 'a' 'word' 'document']
        * *corpus* is a ``list`` of ``lists``    ex. [['this' 'is' 'a' 'word' 'document']['document' 'two']]
    """
    return tf(token, doc) * idf(token, corpus)


def logtfidf(token, doc, corpus):
    """
    Calculates the Log Term Frequency-Inverse Document Frequency of a token
    
        * *token* is a string               ex. 'word'
        * *doc* is a ``list``                 ex. ['this' 'is' 'a' 'word' 'document']
        * *corpus* is a ``list`` of ``lists``    ex. [['this' 'is' 'a' 'word' 'document']['document' 'two']]
    """
    return math.log(tf(token, doc) + 0.5, 2) * idf(token, corpus) # Base 2 Logs


def binary(token, doc):
    """
    Calculates the Binary existence of a token in a document (doc)

    returns 1 if token exists, 0 otherwise
    
        * *token* is a string               ex. 'word'
        * *doc* is a ``list``                 ex. ['this' 'is' 'a' 'word' 'document']
    """
    if token in doc:
        return 1
    else:
        return 0


def tfpdf(token, channels):
    """
    Calculates the Term Frequency * Proportional Document Frequency (TF*PDF ) [Bun2006]_ [Ishzuka2001]_ [Ishzuka2002]_
    
    * *token* is a string
    * *channels* is a ``list`` of ``Channel`` 
    
    """
    wj = 0.0

    for c in channels:
        njc = 0
        for d in c.documents:
            if token in d.terms:
                njc += 1
        wj += normF(token, c) * math.exp(njc / (0.0 + len(c.documents)))

    return wj


def normF(token, channel):
    """
    Calculates the normalized frequency of a term in a channel of documents
    
    see :py:meth:`tfpdf`
    """
    words = []
    dom = Domain(channel.label)
    for doc in channel.documents:
        for phrase in doc.sentences:
            words.extend(phrase.cleanedWords)
            dom.addWords(phrase.cleanedWords)

    sumW = 0.0

    for wd in dom.words:
        sumW += (words.count(wd) / (0.0 + len(words))) ** 2.0

    return (words.count(token) / (0.0 + len(words))) / sumW


def clusterHist(clst):
    """
    Takes a List of DocNodes and returns an histogram of the most common words
    """
    words = {}
    for doc in clst:
        # print " ".join(doc.txt.split())
        wds = cleanString(doc.txt)
        wds = wds.split()
        for wd in wds:
            if wd not in words:
                words[wd] = 1
            else:
                words[wd] += 1
    return sorted(words.items(), key=lambda (k, v): (v, k), reverse=True)


def enClean():
    """
    English Stop Words
    
    
    """
    return ['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also',
            'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be',
            'because', 'been', 'but', 'by', 'can', 'cannot',
            'could', 'dear', 'did', 'do', 'does', 'either', 'else', 'ever',
            'every', 'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he',
            'her', 'hers', 'him', 'his', 'how', 'however',
            'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'let',
            'like', 'likely', 'may', 'me', 'might', 'most', 'must', 'my',
            'neither', 'no', 'nor', 'not', 'of', 'off',
            'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather',
            'said', 'say', 'says', 'she', 'should', 'since', 'so', 'some',
            'than', 'that', 'the', 'their', 'them', 'then',
            'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us',
            'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which',
            'while', 'who', 'whom', 'why', 'will', 'with',
            'would', 'yet', 'you', 'your']


def ptClean():
    """
    Portuguese Stop Words
    """
    preps = ['a', 'ante', u'após', u'até', 'com', 'contra', 'de', 'desde',
             u'é', 'em', 'entre', 'para', 'per', 'perante', 'por', 'sem',
             'sob', 'sobre', u'trás', 'segundo']
    pronomes = ['eu', 'tu', 'ele', 'ela', u'nós', u'vós', 'eles', 'elas']
    artigos = ['a', 'o', 'as', 'os', 'aos', u'às', 'de', 'do', 'dos',
               'da', 'das']
    outros = ['é', 'que', 'quem', 'como', 'uma', 'um']
    out = ['no', 'na', 'nos', 'nas']
    out.extend(preps)
    out.extend(pronomes)
    out.extend(artigos)
    out.extend(outros)
    return out


def esClean():
    """
    Spanish Stop Words
    
    obtained from http://www.ranks.nl/stopwords/spanish.html
    """
    return [u'un', u'una', u'unas', u'unos', u'uno', u'sobre', u'todo',
            u'también', u'tras', u'otro', u'algún', u'alguno', u'alguna',
            u'algunos', u'algunas', u'ser', u'es', u'soy', u'eres',
            u'somos', u'sois', u'estoy', u'esta', u'estamos', u'estais',
            u'estan', u'como', u'en', u'para', u'atras', u'porque', u'por qué',
            u'estado', u'estaba', u'ante', u'antes',
            u'siendo', u'ambos', u'pero', u'por', u'poder', u'puede', u'puedo',
            u'podemos', u'podeis', u'pueden', u'fui', u'fue', u'fuimos',
            u'fueron', u'hacer', u'hago', u'hace', u'hacemos'
        , u'haceis', u'hacen', u'cada', u'fin', u'incluso', u'primero 	desde'
        , u'conseguir', u'consigo', u'consigue', u'consigues', u'conseguimos',
            u'consiguen', u'ir', u'voy', u'va',
            u'vamos', u'vais', u'van', u'vaya', u'gueno', u'ha', u'tener',
            u'tengo', u'tiene', u'tenemos', u'teneis', u'tienen', u'el', u'la',
            u'lo', u'las', u'los', u'su', u'aqui', u'mio',
            u'tuyo', u'ellos', u'ellas', u'nos', u'nosotros', u'vosotros',
            u'vosotras', u'si', u'dentro', u'solo', u'solamente', u'saber',
            u'sabes', u'sabe', u'sabemos', u'sabeis', u'saben',
            u'ultimo', u'largo', u'bastante', u'haces', u'muchos', u'aquellos',
            u'aquellas', u'sus', u'entonces', u'tiempo', u'verdad',
            u'verdadero', u'verdadera 	cierto', u'ciertos',
            u'cierta', u'ciertas', u'intentar', u'intento', u'intenta',
            u'intentas', u'intentamos', u'intentais', u'intentan', u'dos',
            u'bajo', u'arriba', u'encima', u'usar', u'uso', u'usas'
        , u'usa', u'usamos', u'usais', u'usan', u'emplear', u'empleo',
            u'empleas', u'emplean', u'ampleamos', u'empleais', u'valor', u'muy'
        , u'era', u'eras', u'eramos', u'eran', u'modo',
            u'bien', u'cual', u'cuando', u'donde', u'mientras', u'quien',
            u'con', u'entre', u'sin', u'trabajo', u'trabajar', u'trabajas',
            u'trabaja', u'trabajamos', u'trabajais', u'trabajan'
        , u'podria', u'podrias', u'podriamos', u'podrian', u'podriais', u'yo',
            u'aquel']


def frClean():
    """
    Frenc Stop Words
    
    obtained from http://www.ranks.nl/stopwords/french.html
    """
    return [u'alors', u'au', u'aucuns', u'aussi', u'autre', u'avant', u'avec',
            u'avoir', u'bon', u'car', u'ce', u'cela', u'ces', u'ceux',
            u'chaque', u'ci', u'comme', u'comment', u'dans',
            u'des', u'du', u'dedans', u'dehors', u'depuis', u'deux', u'devrait'
        , u'doit', u'donc', u'dos', u'droite', u'début', u'elle', u'elles',
            u'en', u'encore', u'essai', u'est', u'et',
            u'eu', u'fait', u'faites', u'fois', u'font', u'force', u'haut',
            u'hors', u'ici', u'il', u'ils', u'je 	juste', u'la', u'le',
            u'les', u'leur', u'là', u'ma', u'maintenant',
            u'mais', u'mes', u'mine', u'moins', u'mon', u'mot', u'même', u'ni',
            u'nommés', u'notre', u'nous', u'nouveaux', u'ou', u'où', u'par',
            u'parce', u'parole', u'pas', u'personnes',
            u'peut', u'peu', u'pièce', u'plupart', u'pour', u'pourquoi',
            u'quand', u'que', u'quel', u'quelle', u'quelles', u'quels', u'qui',
            u'sa', u'sans', u'ses', u'seulement', u'si',
            u'sien', u'son', u'sont', u'sous', u'soyez 	sujet', u'sur',
            u'ta', u'tandis', u'tellement', u'tels', u'tes', u'ton', u'tous',
            u'tout', u'trop', u'très', u'tu', u'valeur',
            u'voie', u'voient', u'vont', u'votre', u'vous', u'vu', u'ça',
            u'étaient', u'état', u'étions', u'été', u'être']
