from django import forms
from .models import CSVData, Question, Answer

class UploadCSVForm(forms.ModelForm):
    csv_file = forms.FileField()

    class Meta:
        model = CSVData
        fields = ['csv_file']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'question_type']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = []  # Start with an empty list of fields

    def __init__(self, *args, csv_data_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if csv_data_id:
            questions = Question.objects.filter(csv_data_id=csv_data_id)
            for question in questions:
                field_name = f'question_{question.id}'
                self.fields[field_name] = forms.CharField(
                    label=question.question_text, required=True
                )