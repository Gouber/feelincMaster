import dataclasses
import json
from dataclasses import dataclass

# This will be expanded in the future as more fields are added when more transformers are used
@dataclass
class TweetData:
    text: str
    cashtags: dict
    hashtags: dict
    mentions: dict
    urls: dict
    annotations: dict
    curatedText: str
    sentiment_analysis: dict
    created_at: str

    def __init__(self,
                 text: str = None,
                 cashtags: dict = None,
                 mentions: dict = None,
                 urls: dict = None,
                 hashtags: dict = None,
                 annotations: dict = None,
                 curatedText: str = None,
                 sentiment_analysis: dict = None,
                 created_at: str = None
                 ):
        self.text = text
        self.cashtags = cashtags
        self.mentions = mentions
        self.urls = urls
        self.hashtags = hashtags
        self.annotations = annotations
        self.curatedText = curatedText
        self.sentiment_analysis = sentiment_analysis
        self.created_at = created_at

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)