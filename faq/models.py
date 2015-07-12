import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from managers import QuestionManager

User = get_user_model()

class Topic(models.Model):
    """
    Generic Topics for FAQ question grouping
    """
    name = models.CharField(_('name'), max_length=150)
    slug = models.SlugField(_('slug'), max_length=150)
    sort_order = models.IntegerField(_('sort order'), default=0,
        help_text=_('The order you would like the topic to be displayed.'))

    def get_absolute_url(self):
        return '/faq/' + self.slug

    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")
        ordering = ['sort_order', 'name']

    def __unicode__(self):
        return self.name

class SubTopic(models.Model):
    """
    Generic Subtopics for FAQ question grouping
    """
    name = models.CharField(_('name'), max_length=150)
    slug = models.SlugField(_('slug'), max_length=150)
    sort_order = models.IntegerField(_('sort order'), default=0,
        help_text=_('The order you would like the subtopic to be displayed.'))
    topic = models.ForeignKey(Topic, related_name='subtopics')

    def get_absolute_url(self):
        return '/faq/' +self.topic.slug + '/' + self.slug

    class Meta:
        verbose_name = _("SubTopic")
        verbose_name_plural = _("SubTopics")
        ordering = ['sort_order', 'name']

    def __unicode__(self):
        return self.name

class Question(models.Model):
    HEADER = 2
    ACTIVE = 1
    INACTIVE = 0
    STATUS_CHOICES = (
        (ACTIVE,    _('Active')),
        (INACTIVE,  _('Inactive')),
        (HEADER,    _('Group Header')),
    )
    
    text = models.TextField(_('question'), help_text=_('The actual question itself.'))
    answer = models.TextField(_('answer'), blank=True, help_text=_('The answer text.'))
    topic = models.ForeignKey(Topic, verbose_name=_('topic'), related_name='questions')
    subtopic = models.ForeignKey(SubTopic, verbose_name=_('subtopic'), 
                                 related_name='questions', null=True, 
                                 blank=True)
    slug = models.SlugField(_('slug'), max_length=100)
    status = models.IntegerField(_('status'),
        choices=STATUS_CHOICES, default=ACTIVE, 
        help_text=_("Only questions with their status set to 'Active' will be "
                    "displayed. Questions marked as 'Group Header' are treated "
                    "as such by views and templates that are set up to use them."))
    
    sort_order = models.IntegerField(_('sort order'), default=0,
        help_text=_('The order you would like the question to be displayed.'))

    objects = QuestionManager()
    
    class Meta:
        verbose_name = _("Frequent asked question")
        verbose_name_plural = _("Frequently asked questions")
        ordering = ['sort_order']

    def __unicode__(self):
        return self.text

    def save(self, *args, **kwargs):
        # Set the date updated.
        self.updated_on = datetime.datetime.now()
        
        # Create a unique slug, if needed.
        if not self.slug:
            suffix = 0
            potential = base = slugify(self.text[:90])
            while not self.slug:
                if suffix:
                    potential = "%s-%s" % (base, suffix)
                if not Question.objects.filter(slug=potential).exists():
                    self.slug = potential
                # We hit a conflicting slug; increment the suffix and try again.
                suffix += 1
        
        super(Question, self).save(*args, **kwargs)

    def is_header(self):
        return self.status == Question.HEADER

    def is_active(self):
        return self.status == Question.ACTIVE
