# Generated by Django 4.2.7 on 2023-11-25 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('palteforme', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='content',
            field=models.FileField(upload_to='materials/'),
        ),
    ]
