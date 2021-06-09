import unittest

from tunnels.Utils import Utils

class TestUtils(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestUtils, self).__init__(*args, **kwargs)
        self.utils = Utils()

    def test_curate_abcdefghijklm_urls_mentions(self):
        s = "abcdefghijklm"
        entities = {"urls": [{"start": 2, "end": 5}],
                    "mentions": [{"start": 10, "end": 12}]}
        msg = {}
        msg["data"]= {"entities": entities, "text": s}
        tested = self.utils.curate(msg)
        self.assertEqual("abfghijm", tested.curatedText)
        self.assertEqual([{"start": 2, "end": 5}], tested.urls)
        self.assertEqual([{"start": 10, "end": 12}], tested.mentions)
        self.assertEqual(None, tested.hashtags)
        self.assertEqual(None, tested.cashtags)

    def test_curate_abcdefghijklm_just_urls(self):
        s = "abcdefghijklm"
        entities = {"urls": [{"start": 2, "end": 5}, {"start": 10, "end": 13}]}
        msg = {}
        msg["data"]= {"entities": entities, "text": s}
        tested = self.utils.curate(msg)
        self.assertEqual("abfghij", tested.curatedText)
        self.assertEqual([{"start": 2, "end": 5}, {"start": 10, "end": 13}], tested.urls)
        self.assertEqual(None, tested.mentions)
        self.assertEqual(None, tested.hashtags)
        self.assertEqual(None, tested.cashtags)


    def test_curate_abcdefghijklm_just_mentions(self):
        s = "abcdefghijklm"
        entities = {"mentions": [{"start": 2, "end": 5}, {"start": 10, "end": 13}]}
        msg = {}
        msg["data"]= {"entities": entities, "text": s}
        tested = self.utils.curate(msg)
        self.assertEqual("abfghij", tested.curatedText)
        self.assertEqual([{"start": 2, "end": 5}, {"start": 10, "end": 13}], tested.mentions)
        self.assertEqual(None, tested.urls)
        self.assertEqual(None, tested.hashtags)
        self.assertEqual(None, tested.cashtags)

    def test_curate_abcdefghijklm_just_hashtags(self):
        s = "abcdefghijklm"
        entities = {"hashtags": [{"start": 2, "end": 5}, {"start": 10, "end": 13}]}
        msg = {}
        msg["data"]= {"entities": entities, "text": s}
        tested = self.utils.curate(msg)
        self.assertEqual("abfghij", tested.curatedText)
        self.assertEqual([{"start": 2, "end": 5}, {"start": 10, "end": 13}], tested.hashtags)
        self.assertEqual(None, tested.urls)
        self.assertEqual(None, tested.mentions)
        self.assertEqual(None, tested.cashtags)

    def test_curate_abcdefghijklm_just_cashtags(self):
        s = "abcdefghijklm"
        entities = {"cashtags": [{"start": 2, "end": 5}, {"start": 10, "end": 13}]}
        msg = {}
        msg["data"]= {"entities": entities, "text": s}
        tested = self.utils.curate(msg)
        self.assertEqual("abfghij", tested.curatedText)
        self.assertEqual([{"start": 2, "end": 5}, {"start": 10, "end": 13}], tested.cashtags)
        self.assertEqual(None, tested.urls)
        self.assertEqual(None, tested.hashtags)
        self.assertEqual(None, tested.mentions)

    def test_curate_abcdefghijklm_in_all_categories(self):
        s = "Hi,mynameisVladandIamwritingalotoftests"
        entities = {"cashtags":[{"start":11,"end":15}],
                    "hashtags":[{"start":18,"end":19}],
                    "urls":[{"start":29,"end":32}],
                    "mentions":[{"start":34,"end":39}]
                    }
        msg = {}
        msg["data"]= {"entities": entities, "text": s}
        tested = self.utils.curate(msg)
        self.assertEqual("Hi,mynameisandamwritingaof", tested.curatedText)
        self.assertEqual([{"start":11,"end":15}], tested.cashtags)
        self.assertEqual([{"start":18,"end":19}], tested.hashtags)
        self.assertEqual([{"start":29,"end":32}], tested.urls)
        self.assertEqual([{"start":34,"end":39}], tested.mentions)

    def test_curate_does_nothing_if_no_entities(self):
        s = "Hi my name is Vlad"
        msg = {}
        msg["data"] = {"text": s}
        tested = self.utils.curate(msg)
        self.assertEqual("Hi my name is Vlad", tested.curatedText)
        self.assertEqual(None, tested.urls)
        self.assertEqual(None, tested.mentions)
        self.assertEqual(None, tested.cashtags)
        self.assertEqual(None, tested.hashtags)


    def test_curate_removes_new_lines(self):
        s = "Hi my name is Vlad.\nI love pizza.\nBut I am too fat to eat pizza.\n"
        msg = {}
        msg["data"] = {"text": s}
        tested = self.utils.curate(msg)
        self.assertEqual("Hi my name is Vlad.I love pizza.But I am too fat to eat pizza.", tested.curatedText)
        self.assertEqual(None, tested.urls)
        self.assertEqual(None, tested.mentions)
        self.assertEqual(None, tested.cashtags)
        self.assertEqual(None, tested.hashtags)