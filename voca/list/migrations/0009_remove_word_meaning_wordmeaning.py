# Generated by Django 5.2 on 2025-05-29 08:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0008_alter_topicword_part_of_speech'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='word',
            name='meaning',
        ),
        migrations.CreateModel(
            name='WordMeaning',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_of_speech', models.CharField(max_length=50)),
                ('meaning', models.TextField()),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meanings', to='list.word')),
            ],
        ),
    ]
