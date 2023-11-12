from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=700)
    author = models.ForeignKey('Profile', max_length=30, editable=False, on_delete=models.PROTECT)
    creation_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', related_name='questions')
    rating = models.IntegerField()
    is_deleted = models.BooleanField(default=False)

class Profile(models.Model):
    user = models.OneToOneField('User', on_delete=models.PROTECT)
    picture = models.ImageField(upload_to='uploads/')
    rating = models.IntegerField()
    is_deleted = models.BooleanField(default=False)

class Answer(models.Model):
    content = models.TextField(max_length=700)
    author = models.ForeignKey('Profile', editable=False, on_delete=models.PROTECT)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)
    rating = models.IntegerField()
    question = models.ForeignKey('Question', on_delete=models.PROTECT)
    is_deleted = models.BooleanField(default=False)

class Tag(models.Model):
    tag_name = models.CharField(primary_key=True, max_length=15)

    RED = 'bg-danger'
    BLUE = 'bg-primary'
    YELLOW = 'bg-warning'
    COLOR_CHOICES = [
        (RED, 'red'),
        (BLUE, 'blue'),
        (YELLOW, 'yellow')
    ]

    tag_color = models.CharField(max_length=10, choices=COLOR_CHOICES, default=BLUE)