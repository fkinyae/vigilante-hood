# Generated by Django 3.2.7 on 2021-09-24 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hood', '0002_neighbourhood'),
    ]

    operations = [
        migrations.RenameField(
            model_name='neighbourhood',
            old_name='location',
            new_name='locality',
        ),
    ]