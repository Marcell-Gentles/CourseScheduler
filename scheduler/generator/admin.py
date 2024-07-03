from django.contrib import admin
from .models import all_models
from django.contrib.auth.models import User

# Register your models here.
for model in all_models:
    if model != User:
        admin.site.register(model)