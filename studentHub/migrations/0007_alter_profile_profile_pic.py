# Generated by Django 4.2.7 on 2023-12-30 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentHub', '0006_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
