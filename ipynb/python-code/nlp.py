import re
import nltk
import unicodedata
import contractions
from bs4 import BeautifulSoup
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.stem import SnowballStemmer, WordNetLemmatizer

class nlp(object):
    
    def __init__(self, text, stopwords):
        self.text = text
        self.text = self._remove_special_characters()
        self.stopword_list = stopwords
        self.lemmatizer = WordNetLemmatizer()
        self.result = ''
        #self.tokens = [token.strip() for token in ToktokTokenizer().tokenize(text)]
 

    # strip html METHOD
    #@staticmethod
    def _strip_html(self):
        
        soup = BeautifulSoup(self.text, "html.parser")
        result = soup.get_text()
        #result = re.sub(r"(<[+>]>)","",
        
        return result
 

    # remove accented character METHOD
    #@staticmethod
    def _remove_accent_character(self):
        
        result = unicodedata.normalize('NFKD', self.text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        return result
    
    
    # expand contractions METHOD
    #@staticmethod
    def _expand_contractions(self):
        
        return contractions.fix(self.text)

    
    # remove special characters METHOD
    #@staticmethod
    def _remove_special_characters(self, remove_digits=True):
        
        # remove special characters
        pattern = r"([^a-zA-z0-9\s])" if not remove_digits else r"([^a-zA-z\s])"
        result = re.sub(pattern, '', self.text)
        
        # remove multiple lines & spaces.
        result = re.sub(r"([\r|\n|\r\n]+)"," ",result)
        result = re.sub(r'( +)', ' ', result)
        result = re.sub(r'([{.(-)!}])',' ',result)
        
        result = result.lower()

        return result
    
    
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
        
        result = self.lemmatizer.lemmatize(self.text,pos='v')
                                      
        return result
    
    
    # remove stopwords
    #@staticmethod
    def _remove_stopwords(self):
        tokens = tokenizer.tokenize(self.text)
        tokens = [token.strip() for token in tokens]
        
        result = [token for token in tokens if token.lower() not in self.stopword_list]
        result = ' '.join(result)
        
        return result

    
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
        
        # Lemmatizer
        self.result = self._lemmatization()
               
        # remove stop words
        self.result = self._remove_stopwords()
        
        return self.result