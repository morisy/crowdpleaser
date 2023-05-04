from django.contrib import admin
from .models import CSVData, CsvDataRow, Question, Answer

class CSVDataAdmin(admin.ModelAdmin):
    pass

class CsvDataRowAdmin(admin.ModelAdmin):
    pass

class QuestionAdmin(admin.ModelAdmin):
    pass

class AnswerAdmin(admin.ModelAdmin):
    pass

admin.site.register(CSVData, CSVDataAdmin)
admin.site.register(CsvDataRow, CsvDataRowAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)