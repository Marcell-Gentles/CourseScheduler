from django.contrib import admin
from .models import __all__

# Register your models here.
for model in __all__:
    admin.site.register(model)