from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.

QUESTIONS = [
        {
            'id': i,
            'title': f'Question ({i})???',
            'content': f'''Lorem ipsum dolor sit amet consectetur adipisicing elit. Provident alias libero reprehenderit possimus, \
dolore modi consequuntur placeat enim error suscipit vitae officiis iure in totam dignissimos nulla eius, quaerat aliquid ({i})?'''
        } for i in range(30)
    ]


def paginate(objects, page, per_page=5):
    paginator = Paginator(objects, per_page)
    return paginator.page(page).object_list


def index(request):
    page = int(request.GET.get('page', 1))
    return render(request, 'index.html', {'questions': paginate(QUESTIONS, page)})


def question(request, question_id):
    question_item = QUESTIONS[question_id]
    return render(request, 'question.html', {'question': question_item})


def hot_questions(request):
    return render(request, 'index_hot.html')
