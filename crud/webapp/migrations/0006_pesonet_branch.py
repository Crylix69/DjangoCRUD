# Generated by Django 5.0.4 on 2024-05-10 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_mcregister_branch'),
    ]

    operations = [
        migrations.AddField(
            model_name='pesonet',
            name='branch',
            field=models.CharField(default='Default Branch', max_length=50),
        ),
    ]
