from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    """ Learning_logs homepage """
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """ List all topics """
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)    
   
@login_required
def topic(request, topic_id):
    """ List a single topic and its related entries """
    topic = Topic.objects.get(id=topic_id)
    # Confirm if the topic belongs to the current user
    if topic.owner != request.user:
        raise Http404
        
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)  

@login_required
def new_topic(request):
    """ Add new topic """
    if request.method != 'POST':
        # Not submit data: create a new form
        form = TopicForm()
    else:
        # POST submit data, deal with data
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
        
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)  

@login_required
def new_entry(request, topic_id):
    """ Add new entry for a specific topic """
    topic = Topic.objects.get(id=topic_id)
    
    if request.method != 'POST':
        # Not submit data: create a new form
        form = EntryForm()
    else:
        # POST submit data, deal with data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
        
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)  

@login_required
def edit_entry(request, entry_id):
    """ Edit saved entries """
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        # First request, fill the form with the current entry
        form = EntryForm(instance=entry)
    else:
        # POST submit data, deal with data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
        
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)  
