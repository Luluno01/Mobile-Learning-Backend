import json
from question.models import *

with open('question\Questions\sample\generatedSample.json', encoding='utf-8') as fp:
    ques = json.load(fp)

for q in ques:
    _q = OneChoiceQuestion.create(json=q)
    _q.save()