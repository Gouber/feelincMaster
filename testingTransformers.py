import torch
from transformers import AutoModel, AutoTokenizer, pipeline

from transformers import AutoTokenizer, AutoModelForSequenceClassification


def third_run():
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
    pipe = pipeline("sentiment-analysis", model = model, tokenizer=tokenizer, return_all_scores=True)
    #outputs = model(tokenizer.encode("Imagine literal apes buying $Gme and $doge (this is the best)",return_tensors="pt"))
    #m = torch.nn.Softmax(dim=1)
    #predictions = m(outputs.logits)
    predictions = pipe(["Stocks are rallying!", "Stocks are going down I am going to lose my house"])
    print(pipe("I think gme is a very good buy. I love it"))
    print(predictions)


def run():
    from transformers import pipeline
    nlp = pipeline("sentiment-analysis")

    result = nlp(["I am so happy","I am so sad","I am very excited about meme stonks. Please give me more"])
    for r in result:
        print(r)
        print("\n")
    #print(type(result))
    #print(result)
    #print(f"label: {result['label']}, with score: {round(result['score'], 4)}")
    # result = nlp("I love you")[0]
    # print(f"label: {result['label']}, with score: {round(result['score'], 4)}")

def second_run():
    from transformers import AutoModelForTokenClassification, AutoTokenizer
    import torch
    model = AutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
    tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
    label_list = [
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
    sequence = ["Hugging Face Inc. is a company based in New York City. Its headquarters are in DUMBO, therefore very" \
               "close to the Manhattan Bridge.", "Facebook is owned by Vlad Nistor? I don't think so. But he does live on 88 Wood Lane"]
    # Bit of a hack to get the tokens with the special tokens
    tokens = tokenizer.tokenize(tokenizer.decode(tokenizer.encode(sequence)))
    inputs = tokenizer.encode(sequence, return_tensors="pt")
    outputs = model(inputs).logits
    predictions = torch.argmax(outputs, dim=2)
    print([(token, label_list[prediction]) for token, prediction in zip(tokens, predictions[0].numpy())])