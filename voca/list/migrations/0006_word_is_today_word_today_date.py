# Generated by Django 5.2 on 2025-05-28 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0005_category_remove_topicword_example_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='is_today',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='word',
            name='today_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
