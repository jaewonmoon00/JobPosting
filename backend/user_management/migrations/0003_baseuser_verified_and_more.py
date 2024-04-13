# Generated by Django 4.2.11 on 2024-04-07 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0002_applicantuser_employeruser'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employeruser',
            name='documents_authenticated',
            field=models.BooleanField(default=False),
        ),
    ]