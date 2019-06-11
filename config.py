# Variables that contain the user credentials to access Twitter API
ACCESS_TOKEN = "1123135624469291008-KR3Sxij2QTOuWhTRBSxGT3fo8zM8X1"
ACCESS_TOKEN_SECRET = "fYHYsge712CS1qlxTOJkOFRtQJYexJgxAj7jpRWeDt3iy"
CONSUMER_KEY = "v2wGdaJ01jOVGHtsKuL4B7qBs"
CONSUMER_SECRET = "ekGREAz877UN6HMw5DBrP2f0aIR3jAFfnclSO9HZOImo4BdPQE"


# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
# Model Link
MODEL_WORKPLACE = './ipynb/models/'
MODEL_VEC = MODEL_WORKPLACE + 'lda_tfidf_uni_c_dill.pkl'
MODEL_GENSIM = MODEL_WORKPLACE + 'gensim_model_dill.pkl'

# Vectorizer Link
VECTORIZER_WORKPLACE = './ipynb/vectorizer/'
VECTORIZER = VECTORIZER_WORKPLACE + 'tfidf_uni.vector'

# Dataframe Link
DATAFRAME_WORKPLACE = './ipynb/dataframe/'
DATAFRAME = DATAFRAME_WORKPLACE + 'tfidf_uni.csv'



# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
# Dictionary (Gensim) Link
DICTIONARY = MODEL_WORKPLACE + 'gensim_dictionary.dict'

# Bag Of Words
BOW_CORPUS = MODEL_WORKPLACE + 'gensim_bow_corpus.mm'