from django.urls import path
from . import views

app_name = 'crowdsourcing_app'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('create_question/<int:csv_data_id>/', views.create_question, name='create_question'),
    path('submit_answer/<int:question_id>/', views.submit_answer, name='submit_answer'),
    path('view_progress/<int:csv_data_id>/', views.view_progress, name='view_progress'),
    path('create_question/<int:pk>/launch/', views.launch_crowdsource, name='launch_crowdsource'),
    path('answer_form/<int:csv_data_id>/', views.answer_form, name='answer_form'),
    path('success/', views.success_page, name='success_page'),
]