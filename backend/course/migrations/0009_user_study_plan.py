# Generated by Django 3.2.22 on 2023-10-27 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_gptusage'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='study_plan',
            field=models.TextField(blank=True, null=True),
        ),
    ]
