from django.shortcuts import render

# Create your views here.

QUESTIONS = [
        {
            'id': i,
            'title': f'Question ({i})???',
            'content': f'''Lorem ipsum dolor sit amet consectetur adipisicing elit. Provident alias libero reprehenderit possimus, \
dolore modi consequuntur placeat enim error suscipit vitae officiis iure in totam dignissimos nulla eius, quaerat aliquid ({i})?'''
        } for i in range(10)
    ]


def index(request):
    return render(request, 'index.html', {'questions': QUESTIONS})


def question(request, question_id):
    question_item = QUESTIONS[question_id]
    return render(request, 'question.html', {'question': question_item})


def hot_questions(request):
    return render(request, 'index_hot.html')
