from django.db import models
# from djongo import models

from jsonfield import JSONField

from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser
# Create your models here.


# class ArrayReferenceField(models.ForeignKey):
#     def __init__(self, *args, **kwargs):
#         pass


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    # image = models.ImageField(upload_to='static/img', blank=True, null=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


# class User(AbstractUser):
#     phone = models.CharField(max_length=15)
#     birth_date = models.DateField(null=True, blank=True)
#     address = models.CharField(max_length=200)
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     zipcode = models.CharField(max_length=8)


class Voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # phone = models.CharField(max_length=15)
    # address = models.CharField(max_length=200)
    # city = models.CharField(max_length=100)
    # state = models.CharField(max_length=100)
    # zipcode = models.CharField(max_length=8)
    json = JSONField(default={'"0"':'"0"'})

    def __str__(self):
        return self.user.username
