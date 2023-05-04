from django.db import models
from django.contrib.auth.models import User

class CSVData(models.Model):
    crowdsource_creator = models.ForeignKey(User, on_delete=models.CASCADE)
    original_csv_file = models.FileField(upload_to='csv_files/')

class Question(models.Model):
    csv_data = models.ForeignKey(CSVData, on_delete=models.CASCADE)
    question_text = models.TextField()
    QUESTION_TYPE_CHOICES = [
        ('TF', 'True/False'),
        ('MC', 'Multiple Choice Dropdown'),
        ('FTF', 'Free Text Field'),
        ('FTA', 'Free Text Area'),
    ]
    question_type = models.CharField(
        max_length=3,
        choices=QUESTION_TYPE_CHOICES,
    )

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    crowdsource_contributor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.CharField(max_length=255, null=True, blank=True)
    answer_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    csv_data = models.ForeignKey(CSVData, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.crowdsource_contributor} - {self.answer_text}"


class CsvDataRow(models.Model):
    csv_data = models.ForeignKey(CSVData, on_delete=models.CASCADE)
    data = models.JSONField()

    class Meta:
        verbose_name = 'CSV Data Row'
        verbose_name_plural = 'CSV Data Rows'