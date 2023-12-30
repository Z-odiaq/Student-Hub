# Generated by Django 4.2.7 on 2023-12-28 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentHub', '0003_resource_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='birthday',
            field=models.DateField(default='2000-01-01'),
        ),
        migrations.AddField(
            model_name='profile',
            name='classroom',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='profile',
            name='school',
            field=models.CharField(default='TekUp', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
