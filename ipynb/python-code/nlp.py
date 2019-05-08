import nltk

class NLP(object):
    
    def __init__(self, text=None, tokens=None):
        self.text = text
        self.tokens = self.tokenizer()
    
    def tokenizer(self):
        return nltk.word_tokenize(self.text)

    def stemming(self):
        '''rules-based stemming of a bunch of tokens'''

        new_bag = []
        for token in self.tokens:
            # define rules here
            if token.endswith('s'):
                new_bag.append(token[:-1])
            elif token.endswith('er'):
                new_bag.append(token[:-2])
            elif token.endswith('tion'):
                new_bag.append(token[:-4])
            elif token.endswith('tist'):
                new_bag.append(token[:-4])
            elif token.endswith('ce'):
                new_bag.append(token[:-2])
            elif token.endswith('ing'):
                new_bag.append(token[:-2])
            else:
                new_bag.append(token)

        return new_bag