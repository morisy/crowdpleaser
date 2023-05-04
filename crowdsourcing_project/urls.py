from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from crowdsourcing_app import views
from django.urls import reverse
from crowdsourcing_app.views import custom_404 as custom_404_view

handler404 = custom_404_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('crowdsourcing/', include('crowdsourcing_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),
]