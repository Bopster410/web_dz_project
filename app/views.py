from django.shortcuts import render
from django.core.paginator import Paginator
from app.models import Question, Answer, Tag, Profile

# Create your views here.

def paginate(objects, request, per_page=5):
    page = str(request.GET.get('page', 1))
    page = int(page) if page.isdigit() else 1

    paginator = Paginator(objects, per_page)
    page = 1 if page < 0 else paginator.num_pages if page > paginator.num_pages else page
    return {'page_item': paginator.page(page), 'pages_range': paginator.get_elided_page_range(page, on_each_side=2)}

# New
def index(request):
    questions = Question.objects.newest()
    return render(request, 'index.html', {'page': paginate(questions, request), 'tags': Tag.objects.most_popular(20), 'is_logged_in': True, 'component_to_paginate': 'components/question.html'})

# Hot
def hot_questions(request):
    questions = Question.objects.best()
    return render(request, 'index_hot.html', {'tags': Tag.objects.most_popular(20), 'page': paginate(questions, request), 'component_to_paginate': 'components/question.html'})

# Tag
def tag(request, tag_name):
    try:
        tag_item = Tag.objects.get(pk=tag_name)
    except:
        tag_item = Tag.objects.all()[0]
    questions = Question.objects.with_tag(tag_item.tag_name)
    return render(request, 'index_tags.html', {'tag_item': tag_item, 'tags': Tag.objects.most_popular(20), 'page': paginate(questions, request), 'component_to_paginate': 'components/question.html'})

# Question
def question(request, question_id):
    question_item = Question.objects.with_id(question_id)
    answers = Answer.objects.best(question_id)
    return render(request, 'question.html', {'question': question_item, 'tags': Tag.objects.most_popular(20), 'page': paginate(answers, request), 'component_to_paginate': 'components/answer.html'})

# Log In
def login(request):
    return render(request, 'login.html', {'tags': Tag.objects.most_popular(20)})

# Sign Up
def signup(request):
    return render(request, 'signup.html', {'tags': Tag.objects.most_popular(20)})

# Ask question
def ask(request):
    title = request.GET.get('new_title', 'New title')
    return render(request, 'ask.html', {'tags': Tag.objects.most_popular(20), 'title': title})

# User settings
def settings(request):
    return render(request, 'settings.html', {'tags': Tag.objects.most_popular(20), 'is_logged_in': True})
