# Generated by Django 4.2.7 on 2023-12-24 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_answer_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.FileField(blank=True, default='default_picture', null=True, upload_to='user_pictures/'),
        ),
    ]
