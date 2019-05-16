import nltk
import unicodedata
import contractions
from bs4 import BeautifulSoup
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.stem import SnowballStemmer, PorterStemmer, WordNetLemmatizer

class nlp(object):
    
    def __init__(self, text, stopwords):
        self.text = text
        self.stopword_list = stopwords
        self.lemmatizer = WordNetLemmatizer()
        self.tokens = [token.strip() for token in ToktokTokenizer().tokenize(text)]
    
    # strip html METHOD
    @staticmethod
    def _strip_html(doc):
        
        soup = BeautifulSoup(doc, "html.parser")
        result = soup.get_text()
        return result
    
    # remove accented character METHOD
    @staticmethod
    def _remove_accent_character(doc):
        
        result = unicodedata.normalize('NFKD', doc).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        return result
    
    # expand contractions METHOD
    @staticmethod
    def _expand_contractions(doc):
        
        return contractions.fix(doc)
    
    # sub-function: _expand_contractions()
    # expand matched contractions METHOD
    @staticmethod
    def __expand_contractions_match(self, contraction):
        
        match = contraction.group[0]
        first_char = match[0]
    
    # remove special characters METHOD
    @staticmethod
    def _remove_special_characters(doc, remove_digits=True):
        
        pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
        result = re.sub(pattern, '', doc)
        return result
    
    # Stemming METHOD
    @staticmethod
    def _stemming(doc, stem=True):
        
        if stem:
            stemmer = SnowballStemmer("english")
        else:
            stemmer = PorterStemmer("english")
            
        result = ' '.join([stemmer.stem(word) for word in doc.split()])
        return result
    
    # Lemmatization METHOD
    @staticmethod
    def _lemmatization(doc,lemmatizer=lemmatizer):
        
        result = lemmatizer.lemmatize(doc,pos='v')
                                      
        return result
    
    # remove stopwords
    @staticmethod
    def _remove_stopwords(tokens,stopword_list):
        #tokens = tokenizer.tokenize(text)
        #tokens = [token.strip() for token in tokens]
        
        result = [token for token in tokens if token.lower() not in stopword_list]
        result = ' '.join(result)
        
        return result

    # normalize METHOD
    def normalize(self):
        
        result = self.text
        
        # strip HTML 
        # clear newlines & extra-whitespace
        result = self._strip_html(result)
        result = re.sub("[\r|\n|\r\n]+"," ",result)
        result = re.sub(' +', ' ', result)
        
        # remove accented character
        result = self._remove_accent_character(result)
        
        # expand contractions
        result = self._expand_contractions(result)
        
        # lowercase text
        result = result.lower()
        
        # Lemmatizer
        result = self._lemmatization(result)
        
        # remove special characters
        result = self._remove_special_characters(result)
        
        # remove stop words
        result = self._remove_stopwords(self.tokens,self.stopword_list)
        
        return result