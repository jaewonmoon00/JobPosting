# Generated by Django 4.2.11 on 2024-04-12 00:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_management", "0004_employeruser_verification_in_progress"),
    ]

    operations = [
        migrations.AddField(
            model_name="employeruser",
            name="public_key",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
    ]