from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Department(models.Model):
    name = models.CharField("Department Name", max_length=30)
    course_code = models.CharField(
        "Department code",
        max_length=5,
        unique=True
    )

class Course(models.Model):
    # the campus could be its own model
    campuses = {
        "HM": "MUDD",
        "KS": "SCRIPPS",
        "CM": "CMC",
        "PO": "POMONA",
        "PZ": "PITZER",
        'XX': "Other",
    }
    campus = models.CharField(
        "Offering campus",
        max_length=2,
        choices=campuses,
        default="HM"
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        to_field='course_code',
        default="CSCI"
    )
    code = models.CharField("Numerical course code", max_length=15)

class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # the (usually 1-20) section number
    number = models.CharField("Section number", max_length=10)

class Occurance(models.Model):
    """A single day's occurance of a course, so that different
    days can have different times"""
    section = models.ForeignKey(Section, on_delete=models.CASCADE)            
    days = {
        "M": "Monday",
        "T": "Tuesday",
        "W": "Wednesday",
        "R": "Thursday",
        "F": "Friday"
    }
    day = models.CharField(
        "Day of the week",
        max_length=1,
        choices=days
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

class Schedule(models.Model):
    sections = models.ManyToManyField(Section)
    score = models.DecimalField(
        decimal_places=5,
        max_digits=10
    )


__all__ = [
    Department,
    Course,
    Section,
    Occurance,
    Schedule,
]
