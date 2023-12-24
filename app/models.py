from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class QuestionManager(models.Manager):
    def newest(self):
        return [{'question': q, 'tags': self.get_tags(q.pk)} for q in self.order_by('-creation_date')]
    
    def best(self):
        return [{'question': q, 'tags': self.get_tags(q.pk)} for q in self.order_by('-rating')]
    
    def with_tag(self, tag_name):
        return [{'question': q, 'tags': self.get_tags(q.pk)} for q in self.filter(tags=tag_name)]
    
    def with_id(self, id):
        q = self.get(pk=id)
        return {'question': q, 'tags': self.get_tags(q.pk)}
    
    def get_tags(self, id):
        tag_names = self.values_list('tags', flat=True).filter(pk=id)
        return Tag.objects.filter(pk__in=tag_names)


class Question(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=700)
    author = models.ForeignKey('Profile', max_length=30, on_delete=models.PROTECT)
    creation_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', related_name='questions')
    rating = models.IntegerField()
    is_deleted = models.BooleanField(default=False)

    objects = QuestionManager()

    def __str__(self):
        return f'[{self.pk}]Question "{self.title}"'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    picture = models.FileField(upload_to='user_pictures/', default='default_picture.png', null=True, blank=True)
    rating = models.IntegerField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'[{self.pk}]Profile "{self.user.username}"'


class AnswerManager(models.Manager):
    def newest(self, question_id):
        return self.filter(question=question_id).order_by('-creation_date')

    def best(self, question_id):
        return self.filter(question=question_id).order_by( '-is_correct', '-rating')

class Answer(models.Model):
    content = models.TextField(max_length=700)
    author = models.ForeignKey('Profile', on_delete=models.PROTECT)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)
    rating = models.IntegerField()
    is_deleted = models.BooleanField(default=False)
    question = models.ForeignKey('question', on_delete=models.PROTECT, related_name='answers')

    objects = AnswerManager()

    def __str__(self):
        return f'[{self.pk}]Answer "{self.author.user.username}" on "{self.question.title}"'


class TagManager(models.Manager):
    def most_popular(self, total):
        return self.all()[:total]

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

    objects = TagManager()

    def __str__(self):
        return f'Tag "{self.tag_name}"'