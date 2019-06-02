# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
# Sklearn Stop words
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# NLTK Stop words
from nltk.corpus import stopwords


# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------

# NLP Expected Topics
E_TOPICS = 6

# Split Train & Test
TRAIN_SIZE = 23000
TEST_SIZE = 2000

# stopwords
extra = ['say','england','canada','canadian','wait','walk','even','work','use','healthcare','work','now']
M_STOP_WORDS = ENGLISH_STOP_WORDS.union(extra)

M_STOP_WORDS_NLTK = stopwords.words('english')
M_STOP_WORDS_NLTK.extend(extra)


# GridSearchCV
N_COMPONENTS = [6, 10, 15, 20, 25, 30, 50]
LEARNING_DECAY = ['.3','.5','.7','.9']