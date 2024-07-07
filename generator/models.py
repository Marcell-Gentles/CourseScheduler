from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint

from datetime import datetime, time as dt_time
import copy
from typing import Self

from .constants import *

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
        MUDD: "MUDD",
        SCRIPPS: "SCRIPPS",
        CMC: "CMC",
        POMONA: "POMONA",
        PITZER: "PITZER",
        OTHER: "Other",
    }
    campus = models.CharField(
        "Offering campus",
        max_length=2,
        choices=campuses,
        default=MUDD
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    # 3 or 4 chars: e.g. 101 or 261R
    number = models.CharField("Course number", max_length=4)
    title = models.CharField("Course title", max_length=100, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                name = "unique_course",
                fields = ["campus", "department", "number"]
            )
        ]

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
        constraints = [
            UniqueConstraint(
                name="unique_priority",
                fields=['user', 'course']
            )
        ]


class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    number = models.CharField("Section number", max_length=3)
    
    def __str__(self):
        return f'{self.course}-{self.number}'
    
    class Meta:
        constraints = [
            UniqueConstraint(
                name = "unique_section",
                fields = ['course', 'number']
            )
        ]
    
    def fits_with(self, other: Self):
        # the following types are not really lists but the iteration is eq.
        self_occurances: list[Occurance] = self.occurance_set.all()
        other_occurances: list[Occurance] = other.occurance_set.all()
        for self_occ in self_occurances:
            for other_occ in other_occurances:
                if (
                    # they meet on the same day of the week
                    self_occ.day == other_occ.day
                    and
                    # now check for conflicting times
                    (
                     # self_occ starts during other_occ
                     (self_occ.start_time >= other_occ.start_time
                      and self_occ.start_time <= other_occ.end_time)
                     or
                     # other_occ starts during self_occ
                     (other_occ.start_time >= self_occ.start_time
                      and other_occ.start_time <= self_occ.end_time))):
                        return False
        return True


class Occurance(models.Model):
    """A single day's occurance of a section, so that different
    days can have different times
    """
    days = {
        MONDAY: "Monday",
        TUESDAY: "Tuesday",
        WEDNESDAY: "Wednesday",
        THURSDAY: "Thursday",
        FRIDAY: "Friday"}
    day = models.CharField(
        "Day of the week",
        max_length=1,
        choices=days)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    class Meta:
        constraints = [
            UniqueConstraint(
                name = "unique_occurance",
                # this only allows for one occurance a day
                fields = ['section', 'day']
            )
        ]

    def __str__(self):
        return (
            f'{self.section} : {self.day} : '
            f'{self.start_time.strftime('%I:%M')}-'
            f'{self.end_time.strftime('%I:%M%p')}'
        )
        
    @classmethod
    def create_regular(cls, section: Section,
                       days: tuple[str],
                       times: tuple[dt_time]):
        for day in days:
            cls.objects.create(day=day, start_time=times[0],
                               end_time=times[1], section=section)

class Schedule(models.Model):
    sections = models.ManyToManyField(Section)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.DecimalField(
        "Priority score", decimal_places=5, max_digits=10,
        blank=True, null=True
    )
    as_of = models.DateTimeField(
        "Last scored", blank=True, null=True
    )
    
    def __str__(self):
        if self.score is None:
            return f"{self.owner}'s unscored schedule"
        else:
            return (f"{self.owner}'s schedule with score {self.score}"
                    f"as of {self.as_of.strftime("%d/%m/%Y, %H:%M:%S")}")
    
    class Meta:
        ordering = ['-score']
    
    def calculate_score(self, save=True):
        priorities = self.owner.coursepriority_set.all()
        total = 0.0
        section: Section    # annotation for for loop
        for section in self.sections.all():
            # if the priority level for that course exists
            if priority := priorities.get(course=section.course).level:
                total += 1 / (priority)
        self.score = total
        self.as_of = datetime.now()
        if save:
            self.save()

    def can_fit(self, other_section: Section):
        section: Section
        for section in self.sections.all():
            if not section.fits_with(other_section):
                return False
        return True

    type _SectionGroupList = list[tuple[list[Section]], bool]
    @classmethod
    def _generate_helper(
        cls, existing_schedule: list[Section], courses_to_add: _SectionGroupList,
                ) -> list[list[Section]]:
        """Makes a list of schedules that contain each course no more than
        one time. No schedule will be made that does not include the
        mandatory courses.
        """
        if courses_to_add == []:          # bottom of recursion
            return [existing_schedule]
        new_schedules: list[list[Section]] = []
        current_course = courses_to_add[0]
        course_sections = current_course[0]
        course_is_mandatory = current_course[1]
        for s1 in course_sections: # from the current course group to add
            fits = True
            for s2 in existing_schedule:
                if not s1.fits_with(s2):
                    fits = False
                    break
            if fits:
                new_schedule = copy.copy(existing_schedule)
                new_schedule.append(s1)
                new_schedules += cls._generate_helper(new_schedule,
                                                      courses_to_add[1:])
        # we also consider not adding the course at all, unless mandatory
        if not course_is_mandatory:
            new_schedules += cls._generate_helper(existing_schedule,
                                                  courses_to_add[1:])
        # now we have reached the end of the recursion
            return new_schedules
    @classmethod
    def generate(cls, user: User):
        courses_to_add: cls._SectionGroupList = []
        priority: CoursePriority
        for priority in user.coursepriority_set.all():
            sections: list[Section] = [s for s in
                                       priority.course.section_set.all()]
            is_mandatory: bool = priority.mandatory
            course_info = (sections, is_mandatory)
            courses_to_add.append(course_info)
        schedules = cls._generate_helper([], courses_to_add)
        for s in schedules:
            sched = Schedule(owner=user)
            sched.save()
            sched.sections.add(*s)
            sched.calculate_score()        

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