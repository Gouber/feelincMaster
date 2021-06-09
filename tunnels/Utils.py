from TweetData.TweetData import TweetData
import datetime

class Utils:
    # Remove Non-ascii letters, urls, @RT and @Name
    # https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1194/reports/custom/15785631.pdf
    def curate(self, msg) -> TweetData:
        data = msg["data"]

        to_return = TweetData()
        to_return.text = data["text"]

        if "entities" not in data:
            to_return.curatedText = data["text"].replace("\n", "").encode("ascii", "ignore").decode("ascii")
            return to_return

        entities = data['entities']

        if "annotations" in entities:
            to_return.annotations = entities["annotations"]

        text = data['text']

        all_to_remove = list()
        if "urls" in entities:
            urls = [(a['start'], a['end']) for a in entities["urls"]]
            all_to_remove += urls
            to_return.urls = entities["urls"]
        if "mentions" in entities:
            mentions = [(a['start'], a['end']) for a in entities["mentions"]]
            all_to_remove += mentions
            to_return.mentions = entities["mentions"]
        if "hashtags" in entities:
            hashtags = [(a['start'], a['end']) for a in entities["hashtags"]]
            all_to_remove += hashtags
            to_return.hashtags = entities["hashtags"]
        if "cashtags" in entities:
            #cashtags = [(a['start'], a['end']) for a in entities["cashtags"]]
            #all_to_remove += cashtags
            to_return.cashtags = entities["cashtags"]
        to_return.created_at = datetime.datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%S.000Z")
        all_to_remove = sorted(all_to_remove, key=lambda x: x[0])
        start = 0
        final_string = ""
        for (s, e) in all_to_remove:
            final_string += text[start:s]
            start = e
        final_string = final_string + text[start:]
        final_string.rstrip('\n')
        to_return.curatedText = final_string.encode("ascii", "ignore").decode("ascii")
        return to_return
