# Generated by Django 5.2.2 on 2025-06-09 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='date_created',
        ),
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(max_length=15),
        ),
    ]
