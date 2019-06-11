import dill
import numpy as np
import pandas as pd
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from config import MODEL_2, VECTORIZER, DATAFRAME
stemmer = SnowballStemmer("english")

# ------------------------------------------------------------------------------------------------------------------
# Initialize Dependencies
# ------------------------------------------------------------------------------------------------------------------
with open(MODEL_2, 'rb') as f:
    h_predictor = dill.load(f)

with open(VECTORIZER, 'rb') as f:
    h_vector = dill.load(f)

h_dictionary = pd.read_csv(DATAFRAME,sep='|')



# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
# Define function to predict topic for a given text document.
def predict_topic(text, nlp=None, vectorizer=h_vector, best_lda_model=h_predictor, df_topic_keywords=h_dictionary):
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