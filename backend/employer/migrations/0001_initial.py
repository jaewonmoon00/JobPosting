# Generated by Django 4.2.11 on 2024-04-09 21:54

from django.db import migrations, models
import django.db.models.deletion
import employer.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jobposting', '0002_populate_category_instances'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployerVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('business_address', models.CharField(max_length=255)),
                ('company_description', models.TextField()),
                ('business_contact_info', models.CharField(max_length=255)),
                ('business_logo', models.ImageField(upload_to=employer.models.employer_file_upload_path)),
                ('file1', models.FileField(upload_to=employer.models.employer_file_upload_path)),
                ('file2', models.FileField(upload_to=employer.models.employer_file_upload_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobposting.employer')),
            ],
        ),
    ]