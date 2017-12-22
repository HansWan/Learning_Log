from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    """ Users' learning topics """
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User)
    
    def __str__(self):
        """ Return text of model """
        return self.text 

class Entry(models.Model):
    """ Learned specific knowledge related to a topic """
    topic = models.ForeignKey(Topic)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'entries'
    
    def __str__(self):
        """ Return text of mode """
        
        return self.text[:50] + "..."
