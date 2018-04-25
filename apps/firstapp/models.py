from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import re
import bcrypt


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthdate = models.DateField()

class Quotes(models.Model):
    author = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name="poster", null=True)
    favorites = models.ManyToManyField(User, related_name="favorites")


    def __repr__(self):
        return "<User object: {} {}>".format(self.poster, self.author)
