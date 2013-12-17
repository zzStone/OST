from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

class Blog(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    cre_date = models.DateTimeField('date created')
    view_track = models.IntegerField(default=0)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

class Post(models.Model):
    blog = models.ForeignKey(Blog)
    title = models.CharField(max_length=200)
    body = models.TextField()
    pub_date = models.DateTimeField('date published')
    mod_date = models.DateTimeField('date modified')
    view_track = models.IntegerField(default=0)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.title

class Tag(models.Model):
    post = models.ForeignKey(Post)
    name = models.CharField(max_length=200)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

class Comments(models.Model):
    post = models.ForeignKey(Post)
    editor = models.CharField(max_length=200)
    body = models.TextField()
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.pub_date
