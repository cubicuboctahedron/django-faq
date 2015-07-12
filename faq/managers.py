from django.db import models
from django.db.models.query import QuerySet

class QuestionQuerySet(QuerySet):
    def active(self):
        """
        Return only "active" (i.e. published) questions.
        """
        return self.filter(status__exact=self.model.ACTIVE)

    def without_subtopic(self):
        """
        Return only questions without a subtopic specified.
        """
        return self.filter(subtopic__isnull=True)

class QuestionManager(models.Manager):
    def get_query_set(self):
        return QuestionQuerySet(self.model)

    def active(self):
        return self.get_query_set().active()

    def wihout_subtopic(self):
        return self.get_query_set().without_subtopic()
