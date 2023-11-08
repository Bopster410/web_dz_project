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

# TODO add USERS table

ANSWERS = [
    {
        'id': i,
        'content': '''Lorem ipsum dolor sit amet consectetur adipisicing elit. Provident \
            alias libero reprehenderit possimus, dolore modi consequuntur placeat enim error \
            suscipit vitae officiis iure in totam dignissimos nulla eius, quaerat aliquid?''',
        'rating': randint(-40, 40),
        'is_correct': i == 0
    } for i in range(5)
]

# TODO add rating
QUESTIONS = [
    {
        'id': i,
        'title': f'Question ({i})???',
        'tags': [tag for tag in list(TAGS.values())[::3]],
        'answers': ANSWERS,
        'content': f'''Lorem ipsum dolor sit amet consectetur adipisicing elit. Provident alias libero reprehenderit possimus, \
dolore modi consequuntur placeat enim error suscipit vitae officiis iure in totam dignissimos nulla eius, quaerat aliquid ({i})?'''
    } for i in range(30)
]


def paginate(objects, page, per_page=5):
    paginator = Paginator(objects, per_page)
    return paginator.page(page).object_list

# New
def index(request):
    page = int(request.GET.get('page', 1))
    return render(request, 'index.html', {'questions': paginate(QUESTIONS, page), 'tags': TAGS.values()})

# Hot
def hot_questions(request):
    page = int(request.GET.get('page', 1))
    return render(request, 'index_hot.html', {'tags': TAGS.values(), 'questions': paginate(QUESTIONS, page)})

# Tag
def tag(request, tag_name):
    # TODO send to another page if tag doesn't exist
    tag_item = TAGS[tag_name] if tag_name in TAGS else TAGS['Animals']
    questions = [QUESTIONS[i] for i in range(len(QUESTIONS)) if i % 3 == 0]
    return render(request, 'index_tags.html', {'tag_item': tag_item, 'tags': TAGS.values(), 'questions': questions})

# Question
def question(request, question_id):
    # TODO send to another page if question_id is incorrect
    question_item = QUESTIONS[question_id] if 0 <= question_id and question_id < len(QUESTIONS) else QUESTIONS[0]
    return render(request, 'question.html', {'question': question_item, 'tags': TAGS.values()})

def login(request):
    return render(request, 'login.html', {'tags': TAGS.values()})

def signup(request):
    return render(request, 'signup.html', {'tags': TAGS.values()})

def ask(request):
    title = request.GET.get('new_title', '')
    return render(request, 'ask.html', {'tags': TAGS.values(), 'title': title})

def settings(request):
    return render(request, 'settings.html', {'tags': TAGS.values()})
