from datetime import time
from datatypes import Schedule, Section
from typing import Callable
import json
from io import TextIOWrapper


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
    def predicate(schedule: Schedule):
        for filter in filters:      # Test each filter to pass all of them
            if not filter(schedule):
                return False
        return True
    return predicate


class Filterer:
    """A class to maintain information about the filtering happening in
    the user's browsing session.
    """
    def __init__(self):
        self.filter = lambda schedule: True
        self.filters: list[tuple[Callable, dict[str, str|list|dict]]] = []

    def __repr__(self):
        s = ''
        for i, filter in enumerate(self.filters):
            info = filter[1]
            s += str(i) + ': kind: ' + info['kind'] + ' || args: ' \
                        + str(info['args'])  + ' || kwargs:'\
                        + str(info['kwargs']) + '\n'
        return s
         
    def add(self, kind: str, args: list = [], kwargs: dict = {}):
        """Add an active filter.
        
        Give the following arguments:
        
        kind: the string indicating the type of filter.

        args: the list arguments for constructing that filter, if they exist.

        kwargs: the dictionary of keyword arguments for constructing that
                filter, if they exist.

        Can recieve arguments of the forms .add('kind', [args], {kwargs}),
        .add('kind', [args]), or .add('kind', kwargs={kwargs}), but not
        .add('kind', {kwargs}).

        To make things easier to remember, you can speciy passing arguments:
        .add(kind='kind', args=[args], kwargs={kwargs}) where args and kwargs
        are optional.

        These are the valid arguments to pass ('kind' : (kw)args):

        'time' : start=start_time, end=end_time (HHMM) (these are kwargs)

        'score' : minimum_score

        'courses_I' : courses <section.course string>

        'courses_X' : courses <section.course string>

        'sections_I' : [course<str>, section<str>]   # each arg is a list

        'sections_X' : [course<str>, section<str>]   # must match exactly
        """
        predicate = make_filter(kind, *args, **kwargs)
        self.filters.append((predicate,
                            {'kind': kind,
                             'args': args,
                             'kwargs': kwargs}))
        self.filter = layer_filters(self.filter, predicate)

    def remove(self, filter_info: dict[str, str|list|dict] | int):
        """Remove from the active filters.
        
        Pass the dictionary with all of the information about that filter
        which is stored in self.filters along with the callable filters
        itself.

        Or pass the index in self.filters of the filter to delete
        
        With i as the index of that filter--info pair in the list
        self.filters, the filter will be located in self.filters[i][1],
        where self.filters[i][0] is the callable filter.
        """
        if type(filter_info) == int:
            del(self.filters[filter_info])
        else:
            for i, filter in enumerate(self.filters):
                if filter[1] == filter_info:
                    del(self.filters[i])
                    break
        self.filter = layer_filters(*[pair[0] for pair in self.filters])
    
    def reset(self):
        """Clears all filters from self."""
        # Must use while loop instead of for loop because del in remove breaks
        # indices.
        while self.filters != []:
            filter_info = self.filters[0][1]
            self.remove(filter_info)

    # add optional file writing handled by the function (json.dump)
    def toJSON(self, f: TextIOWrapper | None = None) -> str | None:
        """Serialize the active filters."""
        info = [pair[1] for pair in self.filters]
        if f is not None:
            json.dump(info, f)
        else:
            return json.dumps(info)

    @classmethod
    def fromJSON(cls, js: str | TextIOWrapper):
        """Deserialize saved filters."""
        if type(js) == str:
            info = json.loads(js)
        else:
            info = json.load(js)
        filterer = cls()
        for filter in info:
            filterer.add(**filter)
        return filterer
