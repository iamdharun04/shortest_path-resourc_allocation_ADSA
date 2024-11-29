from django.urls import path
from . import views

urlpatterns = [
    path('plan_tour/', views.plan_tour, name='pt'),  # URL for the tour planning form
]