from django.shortcuts import render

# Create your views here.


def index(request):
    questions = [
        {
            'id': i,
            'title': f'Question ({i})???',
            'content': f'''Lorem ipsum dolor sit amet consectetur adipisicing elit. Provident alias libero reprehenderit possimus, \
dolore modi consequuntur placeat enim error suscipit vitae officiis iure in totam dignissimos nulla eius, quaerat aliquid ({i})?'''
        } for i in range(10)
    ]

    return render(request, 'index.html', {'questions': questions})


def hot_questions(request):
    return render(request, 'index_hot.html')
