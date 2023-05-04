This Django-based crowdsourcing app allows users to upload a CSV file, create questions based on the data in the file, and collect answers from contributors. The app is designed with novice developers in mind and aims to provide a simple and straightforward experience for users.

# Key Features

**1** **CSV File Upload**: Users can upload a CSV file containing the data they want to use as a basis for their crowdsourcing project.
**2** **Question Creation**: After uploading a CSV file, users can create questions that will be answered by contributors.
**3** **Answer Collection**: Contributors can submit answers to the questions created by users.
**4** **Project Progress**: Users can view the progress of their crowdsourcing project, including the number of answers submitted.

# How It Works

## Models

The app uses the following models to store data:

* CSVData: Represents an uploaded CSV file.
* CsvDataRow: Represents a single row of data in a CSV file.
* Question: Represents a question created by a user based on the data in a CSV file.
* Answer: Represents an answer submitted by a contributor.

## Views

The app includes several views for handling the different features:

* upload_csv: Handles the CSV file upload process.
* create_question: Allows users to create questions based on the data in a CSV file.
* submit_answer: Allows contributors to submit answers to questions.
* view_progress: Allows users to view the progress of their crowdsourcing project.
* register: Handles user registration.
* answer_form: Displays the form for submitting answers to questions.
* launch_crowdsource: Generates a URL for contributors to access the answer form.
* success_page: Displays a success message after contributors submit their answers.

## Templates

The app uses several templates for rendering the HTML content:

* base.html: A base template that includes common elements like headers and footers.
* upload_csv.html: Template for uploading a CSV file.
* create_question.html: Template for creating questions.
* submit_answer.html: Template for submitting answers.
* view_progress.html: Template for viewing project progress.
* register.html: Template for user registration.
* answer_form.html: Template for the answer form.
* launch_crowdsource.html: Template for displaying the URL for the answer form.
* success_page.html: Template for displaying the success message after submitting answers.

## Priority Areas for Improvement

**1** **User Interface**: Improve the user interface with better styling and user experience enhancements.
**2** **Authentication**: Implement more robust authentication and authorization systems to protect user data and restrict access to certain features.
**3** **Error Handling**: Improve error handling and provide helpful error messages to users.
**4** **Testing**: Add unit tests and integration tests to ensure the app is functioning correctly.
**5** **Performance**: Optimize the app for better performance, particularly when handling large CSV files or a high number of questions and answers.
**6** **Documentation**: Expand and improve documentation to make it easier for developers to understand and maintain the app.

## Getting Started

To set up the app locally, follow these steps:

1 Clone the repository: git clone https://github.com/yourusername/crowdsourcing_project.git
2 Create and activate a virtual environment: python -m venv venv && source venv/bin/activate
3 Install the requirements: pip install -r requirements.txt
4 Apply migrations: python manage.py migrate
5 Run the development server: python manage.py runserver
6 Access the app in your browser at ~[http://127.0.0.1:8000](http://127.0.0.1:8000/)~