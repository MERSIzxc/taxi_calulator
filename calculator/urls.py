from django.urls import path

from .views import taxi_calculator_view

urlpatterns = [
    path('', taxi_calculator_view, name='taxi_calculator'),
]

