from django.contrib import admin
from forms import QuestionForm
from models import Question, SubTopic, Topic
            
class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    
class SubTopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ['name', 'topic', ]
    
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'sort_order', 'status']
    list_editable = ['sort_order', 'status']
    prepopulated_fields = {'slug':('text',)}
    form = QuestionForm

    def save_model(self, request, obj, form, change): 
        '''
        Update created-by / modified-by fields.
        
        The date fields are upadated at the model layer, but that's not got
        access to the user.
        '''
        # If the object's new update the created_by field.
        if not change:
            obj.created_by = request.user
        
        # Either way update the updated_by field.
        obj.updated_by = request.user

        # Let the superclass do the final saving.
        return super(QuestionAdmin, self).save_model(request, obj, form, change)
        
admin.site.register(Question, QuestionAdmin)
admin.site.register(SubTopic, SubTopicAdmin)
admin.site.register(Topic, TopicAdmin)
