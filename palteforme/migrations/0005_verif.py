# Generated by Django 5.0.2 on 2024-02-17 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('palteforme', '0004_submission_studentname'),
    ]

    operations = [
        migrations.CreateModel(
            name='verif',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('needVerification', models.BooleanField(default=False)),
            ],
        ),
    ]
