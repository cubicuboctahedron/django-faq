from django import forms
from redactor.widgets import RedactorEditor
from .models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        widgets = {'answer': RedactorEditor()}
