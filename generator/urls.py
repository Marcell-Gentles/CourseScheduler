from django.urls import path, include
from . import views

urlpatterns = [
    path('schedules/', views.browse_schedules),         # all
    path('schedules/<int:pk>', views.browse_schedules), # one (detail)
    path('schedules/create/', views.generate_schedules),
    path('priorities/', views.set_priorities),          # create
    path('priorities/<int:pk>', views.set_priorities),  # edit
    # temporary
    path("", views.set_priorities),
]
