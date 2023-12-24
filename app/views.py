from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.forms.models import model_to_dict
from app.models import Question, Answer, Tag, User
from app.forms import LoginForm, UserRegistrationForm, SettingsForm, AskQuestionForm, AnswerForm


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
    return render(request, 'index.html', {'page': paginate(questions, request), 'tags': Tag.objects.most_popular(20), 'user': request.user, 'component_to_paginate': 'components/question.html'})

# Hot
def hot_questions(request):
    questions = Question.objects.best()
    return render(request, 'index_hot.html', {'tags': Tag.objects.most_popular(20), 'page': paginate(questions, request),  'user': request.user,'user': request.user, 'component_to_paginate': 'components/question.html'})

# Tag
def tag(request, tag_name):
    try:
        tag_item = Tag.objects.get(pk=tag_name)
    except Tag.DoesNotExist:
        tag_item = Tag.objects.all()[0]
    questions = Question.objects.with_tag(tag_item.tag_name)
    return render(request, 'index_tags.html', {'tag_item': tag_item, 'tags': Tag.objects.most_popular(20), 'user': request.user, 'page': paginate(questions, request), 'component_to_paginate': 'components/question.html'})

# Question
@csrf_protect
def question(request, question_id):
    user = request.user
    question_item = Question.objects.with_id(question_id)

    if request.method == 'GET':
        answer_form = AnswerForm()
    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer_form.save(profile=user.profile, question=question_item['question'])
            return redirect('question', question_id=question_id)

    answers = Answer.objects.best(question_id)
    return render(request, 'question.html', {'question': question_item, 'tags': Tag.objects.most_popular(20), 'form': answer_form, 'user': user, 'page': paginate(answers, request), 'component_to_paginate': 'components/answer.html'})

# Log In
@csrf_protect
def log_in(request):
    if request.method == 'GET':
        login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next', '/'))
            else:
                login_form.add_error(None, "Wrong password or user doesn't exist!")
                login_form.style_form_error()
            
    return render(request, 'login.html', {'form': login_form, 'user': request.user, 'tags': Tag.objects.most_popular(20)})

def log_out(request):
    logout(request)
    return redirect('log_in')

# Sign Up
@csrf_protect
def signup(request):
    if request.method == 'GET':
        signup_form = UserRegistrationForm()
    if request.method == 'POST':
        signup_form = UserRegistrationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next', '/'))
            else:
                signup_form.add_error(None, "Wrong password or user doesn't exist!")

    return render(request, 'signup.html', {'form': signup_form, 'user': request.user, 'tags': Tag.objects.most_popular(20)})

# Ask question
@login_required(login_url='log_in')
@csrf_protect
def ask(request):
    if request.method == 'GET':
        title = request.GET.get('new_title', 'New title')
        question_form = AskQuestionForm(initial={'title': title})
    if request.method == 'POST':
        question_form = AskQuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(profile=request.user.profile)
            return redirect('question', question_id=question.id)
    return render(request, 'ask.html', {'tags': Tag.objects.most_popular(20), 'user': request.user, 'form': question_form})

# User settings
@login_required(login_url='log_in')
def settings(request):
    user = request.user
    if request.method == 'GET':
        profile_form = SettingsForm(initial=model_to_dict(user))
    if request.method == 'POST':
        profile_form = SettingsForm(request.POST, request.FILES, instance=request.user)
        if profile_form.is_valid():
           profile_form.save() 

    return render(request, 'settings.html', {'form': profile_form,  'user': request.user,'tags': Tag.objects.most_popular(20), 'is_logged_in': True})
