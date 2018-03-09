var template = {
	"question_text": "ques",
	"choices": [
		{
			"choice_text": ""
		},
		{
			"choice_text": ""
		},
		{
			"choice_text": ""
		},
		{
			"choice_text": ""
		}
	],
	"answer": 0,
	"category": 10,
	"source": "",
	"topic": [
		"topic"
	]
};

const SUBJECT = [
  {
    'name': {
      'en': 'primary',
      'zh': '小学'
    },
    'subjects': [
      '语文',
      '数学',
      '英语'
    ]
  },
  {
    'name': {
      'en': 'junior',
      'zh': '初中'
    },
    'subjects': [
      '语文',
      '数学',
      '英语',
      '物理',
      '化学',
      '生物',
      '政治',
      '历史',
      '地理'
    ]
  },
  {
    'name': {
      'en': 'senior',
      'zh': '高中'
    },
    'subjects': [
      '语文',
      '数学',
      '英语',
      '物理',
      '化学',
      '生物',
      '政治',
      '历史',
      '地理'
    ]
  },
  {
    'name': {
      'en': 'undergraduate',
      'zh': '本科'
    },
    'subjects': [
      '高等数学',
      '数据库系统概论',
      '马克思主义基本原理概论'
    ]
  },
  {
    'name': {
      'en': 'postgraduate',
      'zh': '研究生'
    },
    'subjects': [
      '高等数学',
      '数据库系统概论',
      '马克思主义基本原理概论'
    ]
  }
]

const GRADE_SUBJECT_MAP = (function() {
  var map = {};
  SUBJECT.forEach(function(grade, gradeIndex) {
    map[grade.name.zh] = {};
    grade.subjects.forEach(function(subject, subjectIndex) {
      map[grade.name.zh][subject] = '' + (gradeIndex + 1) + subjectIndex;
    });
  });
  return map;
})();

var questions = [];

SUBJECT.forEach(function(grade, gradeIndex) {
	grade.subjects.forEach(function(subject, subjectIndex) {
		for(var j = 0; j < 20; j++) {
			var question_text = '' + Math.floor(Math.random() * 20) + grade.name.zh + subject;
			var choices = [];
			for(var i = 0; i < 4; i++) {
				choices.push({
					choice_text: 'A' + i
				});
			}
			var answer = Math.floor(Math.random() * 4);
			var category = parseInt(GRADE_SUBJECT_MAP[grade.name.zh][subject]);
			var source = 'Ruishen' + grade.name.zh + subject;
			var topic = [];
			for(var i = 0; i < 4; i++) {
				topic.push('topic' + Math.floor(Math.random() * 10));
			}
			questions.push({
				question_text: question_text,
				choices: choices,
				answer: answer,
				category: category,
				source: source,
				topic: topic
			});
		}
	});
});

const fs = require('fs');

fs.writeFile('generatedSample.json', JSON.stringify(questions, ' ', 2), function(err) {
  if(err) {
    console.error(err);
  } else {
    console.log(questions.length + ' questions generated.');
  }
});