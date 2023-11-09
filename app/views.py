from django.shortcuts import render
from django.core.paginator import Paginator
from random import randint

# Create your views here.
TAGS = {
    'Python': {'name': 'Python', 'bg': 'bg-primary'},
    'Cpp': {'name': 'Cpp', 'bg': 'bg-primary'},
    'Google': {'name': 'Google', 'bg': 'bg-danger'},
    'Bootstrap': {'name': 'Bootstrap', 'bg': 'bg-primary'},
    'Dinner': {'name': 'Dinner', 'bg': 'bg-warning'},
    'Animals': {'name': 'Animals', 'bg': 'bg-warning'},
    'Law': {'name': 'Law', 'bg': 'bg-warning'},
    'git': {'name': 'git', 'bg': 'bg-primary'},
    'Languages': {'name': 'Languages', 'bg': 'bg-danger'},
}

ANSWERS = [
    {
        'id': i,
        'content': '''Lorem ipsum dolor sit amet consectetur adipisicing elit. Provident \
            alias libero reprehenderit possimus, dolore modi consequuntur placeat enim error \
            suscipit vitae officiis iure in totam dignissimos nulla eius, quaerat aliquid?''',
        'rating': randint(-40, 40),
        'is_correct': i == 0
    } for i in range(40)
]

QUESTIONS = [
    {
        'id': i,
        'user': f'Bobo_{i}',
        'tags': [tag for tag in list(TAGS.values())[::3]],
        'rating': randint(-40, 40),
        'title': f'Question ({i})???',
        'content': f'''Lorem ipsum dolor sit amet consectetur adipisicing elit. Provident alias libero reprehenderit possimus, \
dolore modi consequuntur placeat enim error suscipit vitae officiis iure in totam dignissimos nulla eius, quaerat aliquid ({i})?'''
    } for i in range(100)
]


def paginate(objects, request, per_page=5):
    page = str(request.GET.get('page', 1))
    page = int(page) if page.isdigit() else 1

    paginator = Paginator(objects, per_page)
    page = 1 if page < 0 else paginator.num_pages if page > paginator.num_pages else page
    return {'page_item': paginator.page(page), 'pages_range': paginator.get_elided_page_range(page, on_each_side=2)}

# New
def index(request):
    return render(request, 'index.html', {'page': paginate(QUESTIONS, request), 'tags': TAGS.values(), 'is_logged_in': True, 'component_to_paginate': 'components/question.html'})

# Hot
def hot_questions(request):
    return render(request, 'index_hot.html', {'tags': TAGS.values(), 'page': paginate(QUESTIONS, request), 'component_to_paginate': 'components/question.html'})

# Tag
def tag(request, tag_name):
    tag_item = TAGS[tag_name] if tag_name in TAGS else TAGS['Animals']
    questions = [QUESTIONS[i] for i in range(len(QUESTIONS)) if i % 3 == 0]
    return render(request, 'index_tags.html', {'tag_item': tag_item, 'tags': TAGS.values(), 'page': paginate(questions, request), 'component_to_paginate': 'components/question.html'})

# Question
def question(request, question_id):
    question_item = QUESTIONS[question_id] if 0 <= question_id and question_id < len(QUESTIONS) else QUESTIONS[0]
    return render(request, 'question.html', {'question': question_item, 'tags': TAGS.values(), 'page': paginate(ANSWERS, request), 'component_to_paginate': 'components/answer.html'})

# Log In
def login(request):
    return render(request, 'login.html', {'tags': TAGS.values()})

# Sign Up
def signup(request):
    return render(request, 'signup.html', {'tags': TAGS.values()})

# Ask question
def ask(request):
    title = request.GET.get('new_title', 'New title')
    return render(request, 'ask.html', {'tags': TAGS.values(), 'title': title})

# User settings
def settings(request):
    return render(request, 'settings.html', {'tags': TAGS.values(), 'is_logged_in': True})
