# Generated by Django 5.1.5 on 2025-01-16 23:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_remove_profile_additional_photos'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={},
        ),
        migrations.RemoveField(
            model_name='message',
            name='receiver',
        ),
    ]
