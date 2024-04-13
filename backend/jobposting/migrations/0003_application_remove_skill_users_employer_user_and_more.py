# Generated by Django 4.2.11 on 2024-04-09 21:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0002_applicantprofile_achievement_honors_and_more'),
        ('jobposting', '0002_populate_category_instances'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jobposting.job')),
                ('proile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='profiles.applicantprofile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='skill',
            name='users',
        ),
        migrations.AddField(
            model_name='employer',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Applicant',
        ),
        migrations.DeleteModel(
            name='Skill',
        ),
    ]
