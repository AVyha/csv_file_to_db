from django.db import models


class StartDate(models.Model):
    date = models.DateField()


class Owner(models.Model):
    name = models.CharField(max_length=20)


class Username(models.Model):
    username = models.CharField(max_length=50)
