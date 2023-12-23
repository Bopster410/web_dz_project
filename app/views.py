from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate, login, logout
from app.models import Question, Answer, Tag
from app.forms import LoginForm


# Create your views here.

def paginate(objects, request, per_page=5):
    page = request.GET.get('page', 1)
    paginator = Paginator(objects, per_page)
    try:
        page_item = paginator.page(page)
        page_range = paginator.get_elided_page_range(page, on_each_side=2)
    except (PageNotAnInteger, EmptyPage):
        page_item = paginator.page(1)
        page_range = paginator.get_elided_page_range(1, on_each_side=2)
        
    return {'page_item': page_item, 'pages_range': page_range, 'total_elements': paginator.count}

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
    except Tag.DoesNotExist:
        tag_item = Tag.objects.all()[0]
    questions = Question.objects.with_tag(tag_item.tag_name)
    return render(request, 'index_tags.html', {'tag_item': tag_item, 'tags': Tag.objects.most_popular(20), 'page': paginate(questions, request), 'component_to_paginate': 'components/question.html'})

# Question
def question(request, question_id):
    question_item = Question.objects.with_id(question_id)
    answers = Answer.objects.best(question_id)
    return render(request, 'question.html', {'question': question_item, 'tags': Tag.objects.most_popular(20), 'page': paginate(answers, request), 'component_to_paginate': 'components/answer.html'})

# Log In
def log_in(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect('index')
        # else:
            
    return render(request, 'login.html', {'tags': Tag.objects.most_popular(20)})

def log_out(request):
    logout(request)
    return redirect('login')

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
