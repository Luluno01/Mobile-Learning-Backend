# Generated by Django 2.0.2 on 2018-02-26 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0006_auto_20180225_0051'),
    ]

    operations = [
        migrations.AddField(
            model_name='choicequestion',
            name='accuracy_daily',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='choicequestion',
            name='accuracy_weekly',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='choicequestion',
            name='correct_count_daily',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='choicequestion',
            name='correct_count_weekly',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='visit_count_daily',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='visit_count_weekly',
            field=models.IntegerField(default=0),
        ),
    ]