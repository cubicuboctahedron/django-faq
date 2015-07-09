from django import forms
from suit_ckeditor.widgets import CKEditorWidget
from .models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        widgets = {'answer': CKEditorWidget()}
