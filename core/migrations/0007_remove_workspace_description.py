# Generated by Django 4.1.7 on 2023-05-28 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_task_assossiatedto_workspacemembers_taskmembers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workspace',
            name='description',
        ),
    ]