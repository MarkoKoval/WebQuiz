# Generated by Django 2.1.7 on 2019-03-03 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20190302_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='no name yet', max_length=64, unique=True),
        ),
    ]
