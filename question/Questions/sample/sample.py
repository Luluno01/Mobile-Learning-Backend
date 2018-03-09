import json
from question.models import OneChoiceQuestion

with open('question/Questions/sample/sample.json', encoding='utf8') as fp:
    questions = json.load(fp)

for question in questions:
    if len(question['answer']) == 1:  # One-choice question
        question['answer'] = question['answer'][0]['index']
        _choices = []
        for choice in question['choices']:
            _choices.append({
                'choice_text': choice
            })
        question['choices'] = _choices
        ques = OneChoiceQuestion.create(json=question)
        ques.save()