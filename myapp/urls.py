from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.home, name='home'),            # URL for the home page
    path('about/', views.about, name='about'),    # URL for the about page  # URL for the plan trips page
    path('plan_backpack/', views.gear_planner_view, name='pb'),
    path('tourplan/', include('tourplan.urls')),

]
