# Generated by Django 4.2.7 on 2023-11-12 22:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.FileField(upload_to='uploads/')),
                ('rating', models.IntegerField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tag_name', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('tag_color', models.CharField(choices=[('bg-danger', 'red'), ('bg-primary', 'blue'), ('bg-warning', 'yellow')], default='bg-primary', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField(max_length=700)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('rating', models.IntegerField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('author', models.ForeignKey(editable=False, max_length=30, on_delete=django.db.models.deletion.PROTECT, to='app.profile')),
                ('tags', models.ManyToManyField(related_name='questions', to='app.tag')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=700)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('is_correct', models.BooleanField(default=False)),
                ('rating', models.IntegerField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('author', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='app.profile')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.question')),
            ],
        ),
    ]