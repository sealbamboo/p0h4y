import re
import nltk
import unicodedata
import contractions
from bs4 import BeautifulSoup
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.stem import SnowballStemmer, WordNetLemmatizer

class nlp(object):
    
    def __init__(self, text, tokenizer, stopwords):
        self.text = text
        self.result = text
        self.tokenizer = tokenizer

        self.stopword_list = stopwords
        self.lemmatizer = WordNetLemmatizer()

        #self.tokens = [token.strip() for token in ToktokTokenizer().tokenize(text)]
 

    # strip html METHOD
    #@staticmethod
    def _strip_html(self):
        
        #soup = BeautifulSoup(self.text, "html.parser")
        #result = soup.get_text()
        self.result = re.sub(r"(<[^>]+>)"," ",self.result)
        
        return self.result
 

    # remove accented character METHOD
    #@staticmethod
    def _remove_accent_character(self):
        
        self.result = unicodedata.normalize('NFKD', self.text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        return self.result
    
    
    # expand contractions METHOD
    #@staticmethod
    def _expand_contractions(self):
        
        return contractions.fix(self.text)

    
    # remove special characters METHOD
    #@staticmethod
    def _remove_special_characters(self, remove_digits=False):
        
        self.result = unicodedata.normalize('NFKD', self.result).encode('ascii', 'ignore').decode('utf-8')
        # remove special characters
        # pattern = r"([^a-zA-z0-9\s\'])" if not remove_digits else r"([^a-zA-z\s\'])"
        # self.result = re.sub(pattern, ' ', self.result)
        if remove_digits:
            self.result = re.sub(r"([^a-zA-z0-9\s\'])"," ",self.result)
        else:
            self.result = re.sub(r"([^a-zA-z\s])"," ",self.result)

        # remove multiple lines & spaces.
        self.result = re.sub(r"([\r|\n|\r\n]+)"," ",self.result)
        self.result = re.sub(r"( +)", " ", self.result)
        self.result = re.sub(r"([{.(-)!}])"," ",self.result)
        
        # lowercase all words
        self.result = self.result.lower()

        return self.result
    
    
    # Stemming METHOD
    #@staticmethod
    def _stemming(self, stem=False):
        
        if stem:
            stemmer = SnowballStemmer("english")
        else:
            stemmer = nltk.porter.PorterStemmer()
            
#         result = ' '.join([stemmer.stem(word) for word in self.text.split()])

        return stemmer.stem(self._lemmatization())
    
    
    # Lemmatization METHOD
    #@staticmethod
    def _lemmatization(self):
        
        self.result = self.lemmatizer.lemmatize(self.result,pos='v')
                                      
        return self.result
    
    
    # remove stopwords
    #@staticmethod
    def _remove_stopwords(self):
        tokens = tokenizer.tokenize(self.text)
        tokens = [token.strip() for token in tokens]
        
        self.result = [token for token in tokens if token.lower() not in self.stopword_list]
        self.result = ' '.join(self.result)
        
        return self.result

    
    # normalize METHOD
    def normalize(self):
        
        self.result = self.text
        
        # strip HTML 
        # clear newlines & extra-whitespace
        self.result = self._strip_html()        
        
        # remove accented characters
        self.result = self._remove_accent_character()
        
        # expand contractions
        self.result = self._expand_contractions()
        
        # remove special characters
        self.result = self._remove_special_characters()
        
        # _stemming
        self.result = self._stemming()
               
        # remove stop words
        self.result = self._remove_stopwords()
        
        return self.result