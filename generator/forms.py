from django import forms
from django.forms import ModelForm, formset_factory
from .models import *

class PriorityForm(ModelForm):
    # for a user to enter their priorities
    class Meta:
        model = CoursePriority
        fields = ["course", "level", "mandatory"]

# for creating new data for everyone
class CourseForm(ModelForm):
    # to create a new course
    class Meta:
        model = Course
        fields = ["department", "number", "campus", "title"]
        
class BaseSectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ["course", "number"]

class RegularSectionForm(BaseSectionForm):
    # same times every day it occurs
    days = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                     choices=Occurance.days)

class IrregularSectionForm(BaseSectionForm):
    # day-by-day times
    pass

