from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.

QUESTIONS = [
    {
        'id': i,
        'title': f'Question ({i})???',
        'tags': [{'name': 'Python', 'bg': 'bg-primary'}, {'name': 'Animals', 'bg': 'bg-warning'}, {'name': 'Google', 'bg': 'bg-danger'}],
        'content': f'''Lorem ipsum dolor sit amet consectetur adipisicing elit. Provident alias libero reprehenderit possimus, \
dolore modi consequuntur placeat enim error suscipit vitae officiis iure in totam dignissimos nulla eius, quaerat aliquid ({i})?'''
    } for i in range(30)
]

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


def paginate(objects, page, per_page=5):
    paginator = Paginator(objects, per_page)
    return paginator.page(page).object_list

# New
def index(request):
    page = int(request.GET.get('page', 1))
    return render(request, 'index.html', {'questions': paginate(QUESTIONS, page), 'tags': TAGS.values()})

# Hot
def hot_questions(request):
    return render(request, 'index_hot.html', {'tags': TAGS.values()})

# Tag
def tag(request, tag_name):
    # TODO send to another page if tag doesn't exist
    tag_item = TAGS[tag_name] if tag_name in TAGS else TAGS['Animals']
    questions = [QUESTIONS[i] for i in range(len(QUESTIONS)) if i % 3 == 0]
    return render(request, 'index_tags.html', {'tag': tag_item, 'tags': TAGS.values(), 'questions': questions})

# Question
def question(request, question_id):
    question_item = QUESTIONS[question_id]
    return render(request, 'question.html', {'question': question_item, 'tags': TAGS.values()})
