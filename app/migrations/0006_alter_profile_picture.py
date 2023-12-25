# Generated by Django 4.2.7 on 2023-12-24 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.FileField(blank=True, default='default_picture.png', null=True, upload_to='user_pictures/'),
        ),
    ]