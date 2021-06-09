from tunnels.tunnel_interface import Tunnel
from transformers import AutoModelForTokenClassification, AutoTokenizer
import torch
from collections import deque

#TODO: Needs more logic to cluster parts of the entities
class EntityExtractorTunnel(Tunnel):

    def __init__(self, dest, src="tweets"):
        self.model = AutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
        self.label_list = [
            "O",  # Outside of a named entity
            "B-MISC",  # Beginning of a miscellaneous entity right after another miscellaneous entity
            "I-MISC",  # Miscellaneous entity
            "B-PER",  # Beginning of a person's name right after another person's name
            "I-PER",  # Person's name
            "B-ORG",  # Beginning of an organisation right after another organisation
            "I-ORG",  # Organisation
            "B-LOC",  # Beginning of a location right after another location
            "I-LOC"  # Location
        ]

        super(EntityExtractorTunnel, self).__init__(dest, src)

    # TODO: Batch more together
    def spawn(self):
        # TODO: Only infer every 10 tweets to avoid overkill on the GPU
        queue = deque()
        batch = list()
        for msg in self.src:
            m = msg.value['data']['text'].rstrip('\n')
            if(len(queue) >= 10):
                batch = [item for item in queue]
                inputs = self.tokenizer.encode(batch, return_tensors="pt")
                outputs = self.model(inputs).logits
                predictions = torch.argmax(outputs, dim=2)
                #TODO: Put these predictions in another Kafka topic / persistent db
            else:
                queue.append(m)
