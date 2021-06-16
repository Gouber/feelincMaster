import dataclasses
from typing import List

from TweetData.TweetData import TweetData
from tunnels.Utils import Utils
from tunnels.tunnel_interface import Tunnel
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class BinarySentimentalAnalysisTunnel(Tunnel):

    def __init__(self, dest, src="tweets"):
        tokenizer = AutoTokenizer.from_pretrained("xlnet-base-cased")
        model = AutoModelForSequenceClassification.from_pretrained("xlnet-base-cased")
        self.nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, return_all_scores=True)
        self.utils = Utils()
        super(BinarySentimentalAnalysisTunnel, self).__init__(dest, src)

    # Ideally you call this with ~ 100 tweets (so as to not waste GPU for no reason)
    def annotate_tweets(self, tweet: List[TweetData]) -> List[TweetData]:
        texts = [t.curatedText for t in tweet]
        res = self.nlp(texts)
        for count, value in enumerate(res):
            tweet[count].sentiment_analysis = value
        return tweet

    def spawn(self):
        buffer = list()
        for msg in self.src:
            m = msg.value
            curated = self.utils.curate(m)
            buffer.append(curated)
            if len(buffer) > 5:
                tweets: List[TweetData] = self.annotate_tweets(buffer)
                tweets = [dataclasses.asdict(t) for t in tweets]
                self.collection.insert_many(tweets)
                buffer = list()
                print("Annotated 5")
