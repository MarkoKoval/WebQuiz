from django.urls import path
from . import views


urlpatterns = [
    path("", views.enter, name = 'enter'),
	path('quiz', views.load_quiz, name='quiz'),
    path('enter', views.enter_quiz_app, name="enter-quiz-app"),
    path('load-quiz-info', views.load_quiz_info, name="quiz_info"),
    path('create', views.create_quiz, name="create"),
    path('load-test-pass-info',views.load_test_pass_info,name = "load"),
    path('check', views.check),
    path('statistic/<str:username>',views.statistic)
]