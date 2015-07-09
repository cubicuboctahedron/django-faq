from django.views.generic import ListView
from .models import Topic

class TopicList(ListView):
    model = Topic
    template = "faq/topic_list.html"
    allow_empty = True
    context_object_name = "topics"
