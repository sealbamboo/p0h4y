from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


# create list of stop words
extra_words = ['say','even','use','health','work','now']

M_STOP_WORDS = list(ENGLISH_STOP_WORDS) + extra_words