import re
import dill
import numpy as np
import pandas as pd

# Gensim
import gensim
import gensim.corpora as corpora

# Sklearn Stop words
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# NLTK
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from .config import MODEL_GENSIM, VECTORIZER, DATAFRAME, DICTIONARY, REGEX_URL
stemmer = SnowballStemmer("english")

# ------------------------------------------------------------------------------------------------------------------
# Initialize Dependencies
# ------------------------------------------------------------------------------------------------------------------
with open(MODEL_GENSIM, 'rb') as f:
    h_g_predictor = dill.load(f)

with open(VECTORIZER, 'rb') as f:
    h_vector = dill.load(f)

h_v_dictionary = pd.read_csv(DATAFRAME,sep='|')
h_g_dictionary = corpora.Dictionary.load(DICTIONARY)

# stopwords
extra = ['say','england','canada','canadian','wait','walk','even','work','use','healthcare','work','now']
M_STOP_WORDS = ENGLISH_STOP_WORDS.union(extra)


# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
# Define function to predict topic for a given text document.
def predict_topic(text, nlp=None, vectorizer=h_vector, best_lda_model=h_g_predictor, df_topic_keywords=h_v_dictionary):
    global sent_to_words
    global lemmatization

    # Step 1: Clean with simple_preprocess
    mytext_2 = list(sent_to_words_by_single(text))
    #print(mytext_2)

    # Step 2: Lemmatize
    mytext_3 = lemmatization_by_single(mytext_2, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
    #print(mytext_3)

    # Step 3: Vectorize transform
    mytext_4 = vectorizer.transform(mytext_3)
    #print(type(mytext_4))

    # Step 4: LDA Transform
    topic_probability_scores = best_lda_model.transform(mytext_4)
    # print(topic_probability_scores, np.argmax(topic_probability_scores))
    
    # Get dominant topic for each document
    dominant_topic = np.argmax(df_document_topic.values, axis=1)
    
    topic = df_topic_keywords.iloc[np.argmax(topic_probability_scores), :].values.tolist()
    return topic, topic_probability_scores


# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
def lemmatization_by_single(text, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    doc = nlp(" ".join(text))
    return [(" ".join([stemmer.stem(token.lemma_) if token.lemma_ not in ['-PRON-'] else '' for token in doc if token.pos_ in allowed_postags]))]


# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
def sent_to_words_by_single(sentences):
    result = []
    for token in gensim.utils.simple_preprocess(sentences, deacc=True):
        result.append(token)
    
    return result


# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
# Tokenize and lemmatize for gensim
def preprocess(text):
    result=[]
    for token in gensim.utils.simple_preprocess(text) :
        if token not in M_STOP_WORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
            
    return result


# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
# Lematize depedencies for gensim
def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))


# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
# Split Url out of content
def get_url(sample):
    result = re.search(REGEX_URL, sample)

    if result:
        return result[0]

    return ''


# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
# Split text out of content
def split_txt_form_url(sample):  
    url = get_url(sample)
    if len(url):
        result = sample.replace(url,'')
        result.lstrip().rstrip()
    else:
        result = sample

    return result