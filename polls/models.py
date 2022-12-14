import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    first_name = models.CharField(max_length=254, verbose_name='Имя', blank=False)
    last_name = models.CharField(max_length=254, verbose_name='Фамилия', blank=False)
    username = models.CharField(max_length=254, verbose_name='Логин', unique=True, blank=False)
    email = models.CharField(max_length=254, verbose_name='Почта', unique=True, blank=False)
    password = models.CharField(max_length=254, verbose_name='Пароль', blank=False)
    avatar = models.ImageField(upload_to='polls/user', verbose_name='Аватарка', blank=False)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.first_name


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    short_description = models.CharField(max_length=400, null=True)
    description = models.CharField(max_length=3000, null=True)
    image = models.ImageField(upload_to='media/questions', blank=True)
    votes = models.IntegerField(default=0, blank=True)
    voted_by = models.ManyToManyField(User, related_name='voted_by', blank=True)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def get_percent(self):
        percents = round(self.votes * 100 / self.question.votes)
        return percents

    def __str__(self):
        return self.choice_text
