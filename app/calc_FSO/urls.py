from django.urls import path
from .views import calc
from django.views.generic import RedirectView

urlpatterns = [
    path('', calc),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico'))
]
