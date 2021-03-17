import json
import numpy as np
class Dataset:
    def __init__(self):
        print('intitailised')
    def Get(self):
        with open('data/DREAM/dev.json') as f:
            ds = json.load(f)
        passage = []
        ques_ans = []
        for d in ds:
            passage.append(''.join(d[0]))
            ques_ans.append(d[1])
        return passage,ques_ans


passage,ques_ans = Dataset().Get()


import torch
from transformers import BertTokenizer, MobileBertForMultipleChoice
from torch.nn.modules import Softmax

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = MobileBertForMultipleChoice.from_pretrained('google/mobilebert-uncased')


correct = 0

for i in range(100):
    fact_sent = passage[i]
    answers = ques_ans[i][0]['choice']
    labels = torch.tensor(0).unsqueeze(0)

    fact_sent = [fact_sent for _ in range(len(answers)) ]

    encoding = tokenizer(list(zip(fact_sent, answers)), return_tensors='pt', padding=True)

    outputs = model(**{k: v.unsqueeze(0) for k,v in encoding.items()}, labels=labels)

    loss, logits = outputs[:2]


    softmax = Softmax( dim=1)
    probabilities = softmax(logits)
    pred_asnwer = answers[np.argmax(probabilities.tolist()[0])]

    if pred_asnwer==ques_ans[i][0]['answer']:
        correct += 1
print(correct)