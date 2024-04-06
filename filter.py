from datetime import time
from datatypes import Schedule, Section
from typing import Callable

def make_filter(kind: str, *args, **kwargs) -> Callable:
    """Returns a filter predicate to filter schedules.
    The following arguments are allowed:
    'kind' : (kw)args
    'time' : start=start_time, end=end_time (HHMM)
    'score' : minimum_score
    'courses_I' : courses <section.course string>
    'courses_X' : courses <section.course string>
    'sections_I' : [course<str>, section<str>]   # each arg is a list
    'sections_X' : [course<str>, section<str>]   # must match exactly
    """
    if kind == 'time':
        if len(kwargs) < 1:
            raise ValueError("No start or end time was provided"
                             "for the time filter.")
        # We have to get the start and/or end times from the kwargs times.
        if 'start' in kwargs:
            start = kwargs['start']
        else:
            start = None
        if 'end' in kwargs:
            end = kwargs['end']
        else:
            end = None
        # We convert the start and end times into time objects for comparison.
        if start is not None:
            start = time(int(start[0:2]), int(start[2:4]))
        if end is not None:
            end = time(int(end[0:2]), int(end[2:4]))
        # The predicate compares them to the schedule's times.
        def predicate(schedule: Schedule):
            if start is not None and schedule.start_time < start:
                return False
            if end is not None and schedule.end_time > end:
                return False
            return True
        return predicate
    
    if kind == 'score':
        threshold = args[0]
        def predicate(schedule: Schedule):
            return schedule.score >= threshold
        return predicate
    
    if kind == 'courses_I':
        courses: list[str] = args
        def predicate(schedule: Schedule):
            for section in schedule.sections:
                if section.course in courses:
                    return True
            return False
        return predicate

    if kind == 'courses_X':
        def predicate(schedule):
            # The exclusion version is the opposite of the inclusion version.
            include_filter = make_filter('courses_I', *args)
            return not include_filter(schedule)
        return predicate

    if kind == 'sections_I':
        course_sections: list[list[str, str]] = args
        def predicate(schedule: Schedule):
            for section in schedule.sections:
                if [section.course, section.section] in course_sections:
                    return True
            return False
        return predicate

    if kind == 'sections_X':
        def predicate(schedule):
            # The exclusion version is the opposite of the inclusion version.
            include_filter = make_filter('sections_I', *args)
            return not include_filter(schedule)
        return predicate
    
    raise ValueError("'{}' is not an allowed kind of filter.".format(kind))

def layer_filters(*filters: Callable) -> Callable:
    """Layers filters so that all must be satisfied to pass through."""
    # I start by creating a 'filter' that accpets anything.
    predicate = lambda schedule: True
    # Then I iteritively add each filter to that one
    for filter in filters:
        predicate = lambda schedule: predicate(schedule) and filter(schedule)
    return predicate