""" Define learning_logs URL pattern """

from django.conf.urls import url

from . import views

urlpatterns = [
    # Homepage
    url(r'^$', views.index, name='index'),
    
    # List all topics
    url(r'^topics/$', views.topics, name='topics'),
    
    # Detailed page for a specific topic
    url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    
    # Page to add new topics
    url(r'^new_topic/$', views.new_topic, name='new_topic'),
    
    # Page to add new entries
    url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),

    # Page to edit entries
    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),

]
