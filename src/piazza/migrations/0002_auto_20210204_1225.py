# Generated by Django 3.0.2 on 2021-02-04 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('piazza', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='owner_fullname',
            new_name='name',
        ),
    ]