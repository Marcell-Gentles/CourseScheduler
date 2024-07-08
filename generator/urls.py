from django.urls import path, include
from . import views

urlpatterns = [
    path('make/', views.generate_schedules),
    path('priorities/', views.set_priorities),
    # temporary
    path("", views.set_priorities),
]
