from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot_questions, name='hot'),
    path('tag/<str:tag_name>', views.tag, name='tag'),
    path('question/<int:question_id>', views.question, name='question'),
    path('login/', views.log_in, name='log_in'),
    path('logout/', views.log_out, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('ask/', views.ask, name='ask'),
    path('settings/', views.settings, name='settings'),
    path('question_like/', views.question_like, name='question_like'),
    path('answer_like/', views.answer_like, name='answer_like'),
    path('check_correct/', views.check_correct, name='check_correct'),
]
