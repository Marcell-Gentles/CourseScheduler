from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Department(models.Model):
    name = models.CharField("Department Name", max_length=30)
    # don't make this PK; code could change in the futre
    code = models.CharField("Department code", max_length=4, unique=True)
    def __str__(self):
        return self.name
        # return self.code


class Course(models.Model):
    # the campus could be its own model,
    # but it is only used here
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
        # TODO: remove default if this gets widespread use beyond HMC
        default="HM"
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    # 3 or 4 chars: e.g. 101 or 261R
    number = models.CharField("Course number", max_length=4)
    title = models.CharField("Course title", max_length=100, blank=True)

    def __str__(self):
        return f'{self.department.code}{self.number}{self.campus}'


class CoursePriority(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # A user can assemble a list of desired courses without yet deciding
    # on priorities, but they must choose them before generating schedules
    level = models.SmallIntegerField("Priority level", blank=True, null=True)
    # a user doesn't need a priority if mandatory is true
    mandatory = models.BooleanField("Course is mandatory", default=False)
    def __str__(self):
        return f'{self.user} : {self.course} : {self.level}'
    class Meta:
        verbose_name_plural = "Course Priorities"

class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    number = models.CharField("Section number", max_length=3)
    def __str__(self):
        return f'{self.course}-{self.number}'

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
    def __str__(self):
        return (
            f'{self.section} : {self.day} : '
            f'{self.start_time.strftime('%I:%M')}-'
            f'{self.end_time.strftime('%I:%M%p')}'
        )

class Schedule(models.Model):
    sections = models.ManyToManyField(Section)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.DecimalField(
        "Priority score", decimal_places=5, max_digits=10,
        blank=True, null=True
    )
    as_of = models.DateTimeField(
        "Last scored", auto_now_add=True, blank=True, null=True
    )
    def __str__(self):
        if self.score is None:
            return f"{self.owner}'s unscored schedule"
        else:
            return f"{self.owner}'s schedule with score {self.score} as of {self.as_of.strftime("%d/%m/%Y, %H:%M:%S")}"
    class Meta:
        ordering = ['-score']


all_models = [
    Department,
    Course,
    CoursePriority,
    Section,
    Occurance,
    Schedule,
    User,
]

__all__ = [
    model.__name__ for model in all_models
]