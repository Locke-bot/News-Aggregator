# Generated by Django 3.2.12 on 2022-02-13 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_newspaper_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspaper',
            name='post_thumbnail',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='newspaper',
            name='published',
            field=models.DateField(),
        ),
    ]
