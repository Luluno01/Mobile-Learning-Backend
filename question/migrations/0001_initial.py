# Generated by Django 2.0.2 on 2018-02-28 08:11

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import question.Questions.FillInQuestion
import question.Questions.MultipleChoiceQuestion
import question.Questions.Question
import question.Questions.QuestionList


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.TextField(default='')),
                ('selection_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Cron',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_run', models.DateTimeField(verbose_name='last run time')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('resolution', models.TextField(default='')),
                ('category', models.IntegerField(default=1)),
                ('topic', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(default='', max_length=100), default=question.Questions.Question.__defaultList__, size=None)),
                ('visit_count', models.IntegerField(default=0)),
                ('visit_count_daily', models.IntegerField(default=0)),
                ('visit_count_weekly', models.IntegerField(default=0)),
                ('source', models.TextField(default='')),
                ('entry_date', models.DateTimeField(verbose_name='entry date')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('one_choice_question', django.contrib.postgres.fields.jsonb.JSONField(default=question.Questions.QuestionList.__defaultDict__)),
                ('multiple_choice_question', django.contrib.postgres.fields.jsonb.JSONField(default=question.Questions.QuestionList.__defaultDict__)),
                ('true_or_false_question', django.contrib.postgres.fields.jsonb.JSONField(default=question.Questions.QuestionList.__defaultDict__)),
                ('fill_in_question', django.contrib.postgres.fields.jsonb.JSONField(default=question.Questions.QuestionList.__defaultDict__)),
                ('subjective_question', django.contrib.postgres.fields.jsonb.JSONField(default=question.Questions.QuestionList.__defaultDict__)),
            ],
        ),
        migrations.CreateModel(
            name='ChoiceQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='question.Question')),
                ('accuracy', models.FloatField(default=0)),
                ('correct_count_daily', models.IntegerField(default=0)),
                ('correct_count_weekly', models.IntegerField(default=0)),
            ],
            bases=('question.question',),
        ),
        migrations.CreateModel(
            name='FillInQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='question.Question')),
                ('answer', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(default='', max_length=100), default=question.Questions.FillInQuestion.__defaultList__, size=None)),
            ],
            bases=('question.question',),
        ),
        migrations.CreateModel(
            name='MultipleChoiceChoice',
            fields=[
                ('choice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='question.Choice')),
            ],
            bases=('question.choice',),
        ),
        migrations.CreateModel(
            name='OneChoiceChoice',
            fields=[
                ('choice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='question.Choice')),
            ],
            bases=('question.choice',),
        ),
        migrations.CreateModel(
            name='SubjectiveQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='question.Question')),
                ('answer', models.TextField(default='')),
            ],
            bases=('question.question',),
        ),
        migrations.CreateModel(
            name='TrueOrFalseQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='question.Question')),
                ('answer', models.BooleanField(default=True)),
                ('correct_count', models.IntegerField(default=0)),
                ('correct_count_daily', models.IntegerField(default=0)),
                ('correct_count_weekly', models.IntegerField(default=0)),
            ],
            bases=('question.question',),
        ),
        migrations.CreateModel(
            name='MultipleChoiceQuestion',
            fields=[
                ('choicequestion_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='question.ChoiceQuestion')),
                ('answer', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(default=0), default=question.Questions.MultipleChoiceQuestion.__defaultList__, size=None)),
                ('correct_count', models.IntegerField(default=0)),
            ],
            bases=('question.choicequestion',),
        ),
        migrations.CreateModel(
            name='OneChoiceQuestion',
            fields=[
                ('choicequestion_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='question.ChoiceQuestion')),
                ('answer', models.IntegerField(default=0)),
            ],
            bases=('question.choicequestion',),
        ),
        migrations.AddField(
            model_name='onechoicechoice',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='question.OneChoiceQuestion'),
        ),
        migrations.AddField(
            model_name='multiplechoicechoice',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='question.MultipleChoiceQuestion'),
        ),
    ]
