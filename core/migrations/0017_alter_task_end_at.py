# Generated by Django 4.1.7 on 2023-08-03 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_task_task_brifings_task_task_header'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='end_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
