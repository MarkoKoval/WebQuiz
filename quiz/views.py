from django.shortcuts import render
from django.http import JsonResponse
from .models import Quiz,Question,VariantResult,User,PassedQuiz,QuestionAnswerResult
# Create your views here.
from .quizes_data import *
import os
import ast
import json

def enter(request):
    return render(request, "login.html")


def load_quiz(request):
    print(request.POST)
    return render(request, "quiz.html")


def enter_quiz_app(request):
    user,created = User.objects.get_or_create(name=request.POST["email"],password=request.POST["password"])
    print(user.password)
    print(request.POST["password"])
    if not created:
        if user.password == request.POST["password"]:
            return render(request, "quiz.html",  {"user":user})
        else:

            return render(request, "login.html", {"user":user})

    print(request.POST)
    return render(request, "quiz.html", {"user":user})


def load_quiz_info(request):
    print(request.POST["quiz_name"])

    response = Data.get(request.POST["quiz_name"])
    print(response)
    return JsonResponse(response,safe=False)


def create_quiz(request):
    Quiz.objects.all().delete()
    Question.objects.all().delete()
    VariantResult.objects.all().delete()
    Data = {"beginner": [{
        'question': "•	Переживаєте за успіх в роботі?",
        'choices': ["сильно", "не дуже", "спокійний"],
        'correctAnswer': [5, 3, 2]
    },
        {
            'question': "•	Прагнете досягти швидко результату?",
            'choices': ["поступово", "якомога швидше", "дуже"],
            'correctAnswer': [2, 3, 5]
        },

        {
            'question': "•	Легко попадаєте в тупик при проблемах в роботі?",
            'choices': ["неодмінно", "поступово", "зрідка"],
            'correctAnswer': [5, 3, 2]
        },

        {
            'question': "•	Чи   потрібен чіткий алгоритм для вирішення задач?",
            'choices': ["так", "в окремих випадках", "не потрібен"],
            'correctAnswer': [5, 3, 2]
        },
    ]}
    try:
        quiz = Quiz(title="First Quiz")
        quiz.save()
        for item in Data["beginner"]:
            print(item["question"])
            question = Question(title=item["question"])
            question.save()
            for choice, score in zip(item["choices"], item["correctAnswer"]):
                print(choice+" " + str(score))
                vr = VariantResult(choice=choice, score=score)
                vr.save()
                question.variant_result_pair.add(vr)

            quiz.questions.add(question)
            quiz.save()
    except Exception as exp:
        print(exp)
    return render(request, "test.html", {"quizes": Quiz.objects.all()})


def load_test_pass_info(request):

    result = ast.literal_eval(request.POST["data"])
    quiz_name = result[0]
    print(quiz_name)
    user_name = result[1]
    print(user_name)
    questions = []

    exist_quiz_previously = True
    try:
        item = User.objects.get(name=user_name).passed_quizes.get(quiz_name=quiz_name)#.passed_quizes.all().get(quiz_name=quiz_name)
    except Exception as ex:
        print(ex)
        exist_quiz_previously = False
    print(exist_quiz_previously)
    for i in result[2:]:
        val = ast.literal_eval(i)
        questions.append(val)
        print(val)
    try:

        quiz =  User.objects.get(name=user_name).passed_quizes.get(quiz_name=quiz_name) if exist_quiz_previously else PassedQuiz(quiz_name=quiz_name)
        if not exist_quiz_previously:
            quiz.save()
        else:
            User.objects.get(name=user_name).passed_quizes.get(quiz_name=quiz_name).question_answer_result_pair.all().delete()
        #print("quiz")

        for item in questions:
            obj = QuestionAnswerResult(question=item["question"],answer=item["choices"],result=item["correctAnswer"])
            obj.save()
            #print("question")
            #print(dir(quiz))

            quiz.question_answer_result_pair.add(obj)
            quiz.save()
            #print("questionsss")

        User.objects.get(name=user_name).passed_quizes.add(quiz)
       # print("eerr")
    except Exception as ex:
        print(ex)
    return  render(request, "quiz.html")


def check(request):
     User.objects.all().delete()
     PassedQuiz.objects.all().delete()
     QuestionAnswerResult.objects.all().delete()

     return render(request, "quiz.html")


def statistic(request, username):
    obj = User.objects.get(name=username)
    print(obj.name)
    print(obj.password)

    js = dict()
    for quiz_ in obj.passed_quizes.all():
        print(quiz_.quiz_name)
        js[quiz_.quiz_name] = []
        for que in quiz_.question_answer_result_pair.all():
            js[quiz_.quiz_name].append({"question":que.question,
                                         "answer":que.answer,
                                        "result":que.result})
            print(que.question + " " + que.answer + " " + str(que.result))
    js = json.dumps(js)
    return render(request, "statistic.html", {"user":obj, "js":js})
