from django.db import migrations

def create_categories(apps, schema_editor):
    Category = apps.get_model('jobposting', 'Category')
    Category.objects.update_or_create(name='PT', defaults={'name': 'PT'})
    Category.objects.update_or_create(name='FT', defaults={'name': 'FT'})
class Migration(migrations.Migration):

    dependencies = [
        ('jobposting', '0001_initial'),  # Replace 'your_app_name' and '000x_previous_migration' with correct values
    ]

    operations = [
        migrations.RunPython(create_categories),
    ]
