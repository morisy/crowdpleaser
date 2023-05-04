import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, get_resolver
from django.contrib.auth.decorators import login_required
from .forms import UploadCSVForm, QuestionForm, AnswerForm
from .models import CSVData, CsvDataRow, Question, Answer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
import traceback
import sys
from django.contrib import messages


def home(request):
    return HttpResponse("Hello, welcome to the crowdsourcing project!")

@login_required
def upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_data = form.save(commit=False)
            csv_data.crowdsource_creator = request.user
            csv_data.save()

            csv_file = request.FILES['csv_file']
            reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())

            for row in reader:
                data_row = CsvDataRow(csv_data=csv_data, data=row)
                data_row.save()

            messages.success(request, 'CSV file uploaded successfully.')
            return HttpResponseRedirect(reverse('crowdsourcing_app:create_question', args=[csv_data.id]))
        else:
            messages.error(request, 'Error uploading CSV file. Please check the form and try again.')
    else:
        form = UploadCSVForm()
    return render(request, 'crowdsourcing_app/upload_csv.html', {'form': form})


@login_required
def create_question(request, csv_data_id):
    csv_data = get_object_or_404(CSVData, id=csv_data_id)
    csv_data_row = CsvDataRow.objects.filter(csv_data=csv_data).first()

    if not csv_data_row:
        return HttpResponse('No data available.')

    tags = list(csv_data_row.data.keys())
    example_row = list(csv_data_row.data.values())

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.csv_data_id = csv_data_id
            question.save()
            return HttpResponseRedirect(reverse('crowdsourcing_app:create_question', args=[csv_data_id]))
    else:
        form = QuestionForm()
    
    context = {
        'form': form,
        'tags': tags,
        'example_row': example_row,
        'csv_data': csv_data  # Add the 'csv_data' object to the context
    }
    return render(request, 'crowdsourcing_app/create_question.html', context)


def submit_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    csv_data_row = CsvDataRow.objects.filter(csv_data=question.csv_data, completed=False).first()

    if not csv_data_row:
        return HttpResponse('No more questions available.')

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = Answer(
                question_id=question_id,
                crowdsource_contributor=request.user if request.user.is_authenticated else None,
                ip_address=request.META.get('REMOTE_ADDR') if not request.user.is_authenticated else None,
                answer_text=form.cleaned_data['answer']
            )
            answer.save()
            csv_data_row.completed = True
            csv_data_row.save()
            return HttpResponse('Thanks for your submission!')
    else:
        form = AnswerForm()

    return render(request, 'crowdsourcing_app/submit_answer.html', {'form': form, 'question': question})

@login_required
def view_progress(request, csv_data_id):
    csv_data = CSVData.objects.get(pk=csv_data_id)
    if request.user != csv_data.crowdsource_creator:
        return HttpResponse('You are not authorized to view this page.')

    answers = Answer.objects.filter(question__csv_data=csv_data)
    progress = answers.count() / Question.objects.filter(csv_data=csv_data).count() * 100

    return render(request, 'crowdsourcing_app/view_progress.html', {'answers': answers, 'progress': progress})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('upload_csv'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


from django.http import HttpResponse
import traceback
import sys

def custom_404(request, exception=None):
    # Log the traceback
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback, limit=None, file=sys.stderr)

    # Build the response
    response = HttpResponse("Oops! The requested URL was not found. Here's a list of available URLs:<br>")
    response.write("1. /crowdsourcing/upload_csv/ - Upload a CSV file<br>")
    response.write("2. /crowdsourcing/create_question/&lt;csv_data_id&gt;/ - Create a question based on the uploaded CSV<br>")
    response.write("3. /crowdsourcing/submit_answer/&lt;question_id&gt;/ - Submit an answer for a question<br>")
    response.write("4. /crowdsourcing/view_progress/&lt;csv_data_id&gt;/ - View the progress of the crowdsourcing project<br>")
    response.write("5. /accounts/register/ - Register a new user<br>")
    response.write("6. /accounts/login/ - Log in as an existing user<br>")
    response.write("7. /accounts/logout/ - Log out<br>")
    response.status_code = 404

    return response

def launch_crowdsource(request, pk):
    csv_data = get_object_or_404(CSVData, pk=pk)
    launch_url = reverse('crowdsourcing_app:answer_form', args=[csv_data.id])
    return render(request, 'crowdsourcing_app/launch_crowdsource.html', {'launch_url': launch_url})

def answer_form(request, csv_data_id):
    csv_data = get_object_or_404(CSVData, id=csv_data_id)
    questions = Question.objects.filter(csv_data=csv_data)
    
    if request.method == 'POST':
        form = AnswerForm(request.POST, csv_data_id=csv_data_id)
        if form.is_valid():
            for question in questions:
                field_name = f'question_{question.id}'
                answer_text = form.cleaned_data[field_name]
                answer = Answer(
                    question=question,
                    csv_data=csv_data,
                    crowdsource_contributor=request.user if request.user.is_authenticated else None,
                    ip_address=request.META.get('REMOTE_ADDR') if not request.user.is_authenticated else None,
                    answer_text=answer_text
                )
                answer.save()
            # Redirect or render a template with a success message
            return HttpResponseRedirect(reverse('crowdsourcing_app:success_page'))
    else:
        form = AnswerForm(csv_data_id=csv_data_id)

    context = {
        'form': form,
        'questions': questions,
        'csv_data': csv_data
    }
    return render(request, 'crowdsourcing_app/answer_form.html', context)

def success_page(request):
    return render(request, 'crowdsourcing_app/success_page.html')
