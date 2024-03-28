from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host =  models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    topic = models.ForeignKey(Topic, on_delete = models.SET_NULL, null = True)
    name = models.CharField(max_length=200)
    description = models.TextField(null = True, blank=True) # the user can left it blank
    participants = models.ManyToManyField(User, related_name='participants',  blank = True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-updated','-created'] #newest items first
        # ordering = ['updated','created']  -> newest will be last

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    room = models.ForeignKey(Room, on_delete = models.CASCADE) 
    # This is one to many relation ship which is one parent and many childrens in the database 
    # and models.CASCADE makes delete the child when one deleted the parent 
    body = models.TextField()
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.body[0:50] #only the first 50 characters

