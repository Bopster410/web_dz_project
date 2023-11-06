from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def hot_questions(request):
    return render(request, 'index_hot.html')