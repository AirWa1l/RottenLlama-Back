# Generated by Django 5.1.7 on 2025-03-17 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='reset_password_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
