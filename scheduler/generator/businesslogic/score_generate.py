from ..models import *
import copy
from datetime import datetime

DEFAULT_MAX = 200


type SectionList = list[Section]

def fits_with(section: Section,
              other: Section | SectionList
              ) -> bool:
    """Returns true if the section does not conflict with the other"""
    if type(other) == Section:
        # first check days
        occurances: list[Occurance] = section.occurance_set.all()
        other_occurances: list[Occurance] = other.occurance_set.all()
        for occ in occurances:
            for other_occ in other_occurances:
                if (
                    # they meet on the same day of the week
                    occ.day == other_occ.day
                    and
                    # now check for conflicting times
                    (
                     # occ starts during other_occ
                     (occ.start_time >= other_occ.start_time
                      and occ.start_time <= other_occ.end_time)
                     or
                     # other_occ starts during occ
                     (other_occ.start_time >= occ.start_time
                      and other_occ.start_time <= occ.end_time))):
                        return False
        return True
    elif type(other) == list:
        for other_section in other:
            if not fits_with(section, other_section):
                return False
        return True 
    else:
        raise TypeError("Argument was not a Section or list of them but a "
                        + str(type(other)))

def is_mandatory(course: Course, user: User) -> bool:
    pass

# each list element is associated with a course
# the list in the tuple is the sections of that course
# the bool is whether it is mandatory
type SectionGroupList = list[tuple[list[Section]], bool]
def make_schedules_as_list(
        existing_schedule: list[Section], courses_to_add: SectionGroupList,
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
    for section in course_sections: # from the current course group to add
        if fits_with(section, existing_schedule):
            # add to the list all of the schedules that can be made by
            # including that section
            new_schedule = copy.copy(existing_schedule)
            new_schedule.append(section)
            new_schedules += make_schedules_as_list(new_schedule, courses_to_add[1:])
    # we also consider not adding the course at all, unless mandatory
    if not course_is_mandatory:
        new_schedules += make_schedules_as_list(existing_schedule, courses_to_add[1:])
    # now we have reached the end of the recursion
        return new_schedules

# have this so that they can be scored before even being in database,
# immediately after generation.
def score_schedule_as_list(
    schedule: list[Section],
    mapping: dict[Course, int | None]
        ) -> float:
    score: float = 0.0
    for section in schedule:
        course = section.course
        priority_level = mapping[course]
        if priority_level is not None:
            score += float(1 / priority_level)
    return score

def get_priority_map(user: User):
    course_priorities: list[CoursePriority] = user.coursepriority_set.all()
    return {x.course: x.level for x in course_priorities}


def make_schedules(user: User, max=DEFAULT_MAX):
    """So easy"""
    priority_map = get_priority_map(user)
    courses_as_list: SectionGroupList = []
    for course_priority in user.coursepriority_set.all():
        courses_as_list.append(
            ([section for section in course_priority.course.section_set.all()],
              course_priority.mandatory)
        )
    schedules_as_list = make_schedules_as_list([], courses_as_list)
    score_time = datetime.now()
    scored_schedules = [(schedule, score_schedule_as_list(schedule, priority_map))
                                 for schedule in schedules_as_list]
    scored_schedules.sort(key=lambda x: x[1], reverse=True)
    for schedule in scored_schedules[:max]:
        sch = Schedule(owner=user, score=schedule[1], as_of=score_time)
        sch.save()
        sch.sections.add(*schedule[0])

def score(schedule: Schedule, user: User):
    "Regenerate score"
    priority_map = get_priority_map(user)
    # it's actually a queryset but it should be ok
    schedule_as_list: list[Section] = schedule.sections.all()
    score_time = datetime.now()
    schedule_score = score_schedule_as_list(schedule_as_list, priority_map)
    schedule.score = schedule_score
    schedule.as_of = score_time
    schedule.save()
    
