# Generated by Django 5.0.1 on 2024-02-02 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_authorprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
