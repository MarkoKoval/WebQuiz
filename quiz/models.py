from django.db import models

# Create your models here.


class Quiz(models.Model):
        title = models.CharField(max_length=64,  default="no title yet")
        questions = models.ManyToManyField('Question', blank=True, related_name='posts')


class Question(models.Model):
        title = models.CharField(max_length=64,  default="no title yet")
        variant_result_pair = models.ManyToManyField('VariantResult', blank=True, related_name='posts')


class VariantResult(models.Model):
        choice = models.CharField(max_length=64,  default="no title yet")
        score = models.IntegerField()


class QuestionAnswerResult(models.Model):
        question =  models.CharField(max_length=64,  default="no question yet")
        answer = models.CharField(max_length=64,  default="no question yet")
        result = models.IntegerField()


class PassedQuiz(models.Model):
        quiz_name = models.CharField(max_length=64,  default="no name yet")
        question_answer_result_pair = models.ManyToManyField('QuestionAnswerResult', blank=True, related_name='question_answer_result')


class User(models.Model):
        name = models.CharField(max_length=64,  default="no name yet", unique=True)
        password = models.CharField(max_length=64,  default="no password yet")
        passed_quizes = models.ManyToManyField('PassedQuiz', blank=True, related_name='passed_quizes')

