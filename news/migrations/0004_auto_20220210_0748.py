# Generated by Django 3.2.12 on 2022-02-10 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_newspaper_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newspaper',
            options={'get_latest_by': '-created_at'},
        ),
        migrations.AddField(
            model_name='newspaper',
            name='excerpt',
            field=models.TextField(max_length=50, null=True),
        ),
    ]