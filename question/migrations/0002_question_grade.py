# Generated by Django 2.0.2 on 2018-03-06 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='grade',
            field=models.IntegerField(default=1),
        ),
    ]
