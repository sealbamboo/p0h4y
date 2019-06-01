import config
from sklearn.base import TransformerMixin, BaseEstimator
from nltk.stem import WordNetLemmatizer, SnowballStemmer
stemmer = SnowballStemmer("english")

# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
# Functions
def quick_clean(data):
    
    # remove Email@
    result = re.sub(r"(\S*@\S*\s?)","", data)
    
    # remove website link
    result = re.sub(r"(((http|https):\/\/)?www[a-z\.\/-]+)","website",result)
    
    # Remove new line characters
    result = re.sub(r"\s+", ". ", result)
    
    # Remove distracting single quotes
    result = re.sub(r"\'", "", result)
    
    # Remove Punctuation
    result = re.sub("([^a-zA-Z0-9 ])","",result)
    
    return result


# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations
        
        
# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
def sent_to_words_by_single(sentences):
    result = []
    for token in gensim.utils.simple_preprocess(sentences, deacc=True):
        result.append(token)
    
    return result


# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append(" ".join([stemmer.stem(token.lemma_) if token.lemma_ not in ['-PRON-'] else '' for token in doc if token.pos_ in allowed_postags]))
    return texts_out


# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
def lemmatization_by_single(text, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    doc = nlp(" ".join(text))
    return [(" ".join([stemmer.stem(token.lemma_) if token.lemma_ not in ['-PRON-'] else '' for token in doc if token.pos_ in allowed_postags]))]


# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
# Lematize depedencies for gensim
def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))


# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
# Tokenize and lemmatize for gensim
def preprocess(text):
    result=[]
    for token in gensim.utils.simple_preprocess(text) :
        if token not in config.M_STOP_WORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
            
    return result

# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
def tokenizeText(sample):
    tokens = nlp(sample)
    lemmas = []
    for tok in tokens:
        lemmas.append(tok.lemma_.lower().strip() if tok.lemma_ != "-PRON-" else tok.lower_)
    tokens = lemmas
    tokens = [re.sub(r"([0-9]+)","",tok) for tok in tokens]
    tokens = [tok for tok in tokens if tok not in STOPLIST]
    tokens = [tok for tok in tokens if tok not in SYMBOLS]
    return tokens


# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
class TextPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self,
                 variety="BrE",
                 user_abbrevs={},
                 n_jobs=1):
        """
        Text preprocessing transformer includes steps:
            1. Text normalization
            2. Punctuation removal
            3. Stop words removal
            4. Lemmatization
        
        variety - format of date (AmE - american type, BrE - british format) 
        user_abbrevs - dict of user abbreviations mappings (from normalise package)
        n_jobs - parallel jobs to run
        """
        self.variety = variety
        self.user_abbrevs = user_abbrevs
        self.n_jobs = n_jobs

    def fit(self, X, y=None):
        return self

    def transform(self, X, *_):
        X_copy = X.copy()

        partitions = 1
        cores = mp.cpu_count()
        if self.n_jobs <= -1:
            partitions = cores
        elif self.n_jobs <= 0:
            return X_copy.apply(self._preprocess_text)
        else:
            partitions = min(self.n_jobs, cores)

        data_split = np.array_split(X_copy, partitions)
        pool = mp.Pool(cores)
        data = pd.concat(pool.map(self._preprocess_part, data_split))
        pool.close()
        pool.join()

        return data

    def _preprocess_part(self, part):
        return part.apply(self._preprocess_text)

    def _preprocess_text(self, text):
        normalized_text = self._normalize(text)
        doc = nlp(normalized_text)
        removed_punct = self._remove_punct(doc)
        removed_stop_words = self._remove_stop_words(removed_punct)
        return self._lemmatize(removed_stop_words)

    def _normalize(self, text):
        # some issues in normalise package
        try:
            return ' '.join(normalise(text, variety=self.variety, user_abbrevs=self.user_abbrevs, verbose=False))
        except:
            return text

    def _remove_punct(self, doc):
        return [t for t in doc if t.text not in string.punctuation]

    def _remove_stop_words(self, doc):
        return [t for t in doc if not t.is_stop]

    def _lemmatize(self, doc):
        return ' '.join([t.lemma_ for t in doc])