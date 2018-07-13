from happierfuntokenizing import Tokenizer
from text_worker import TextWorker

from collections import Counter

class FeatureWorker(TextWorker):

    def __init__(self):
        super(FeatureWorker, self).__init__()
        self.tok = Tokenizer()

    def extractNgramPerTweet(self, tweet, n=1):
        """
        Extract n-grams from tweet after standardizing
        """
        tweet = self.shrinkSpace(tweet)
        tweet = self.remove_handles(tweet)
        tweet = self.remove_urls(tweet)
        tokens = self.tok.tokenize(tweet)

        #ngrams = Counter([" ".join(x) for x in zip(*[tokens[i:] for i in range(n)])])
        ngrams = Counter([" ".join(x) for x in zip(*[tokens[n:]])])
        return ngrams

    def fullNGramExtract(self, tweet_list, n=1):
        """
        """
        all_ngrams = Counter()
        for i in range(n):
            this_ngrams = Counter()
            for tweet in tweet_list:
                this_ngrams.update(self.extractNgramPerTweet(tweet, n))
            total_ngrams = float(sum(this_ngrams.values()))
            all_ngrams.update({gram: value / total_ngrams for gram, value in this_ngrams.items()})
        return all_ngrams

    def extractLexicon(self, ngrams, lex, intercepts=None):
        """
        """
        pLex = {} # prob of lex given user
        for term, cats in lex.iteritems():
            try:
                gn = ngrams[term]
                for cat, weight in cats.iteritems():
                    try:
                        pLex[cat] += float(gn)*weight
                    except KeyError:
                        pLex[cat] = float(gn)*weight
            except KeyError:
                pass #not in lex

        if intercepts:
            for cat in intercepts:
                pLex[cat] += intercepts[cat]
        return pLex

