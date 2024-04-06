from datetime import time
import json
import os
from io import TextIOWrapper

PRIORITY_PATH = os.path.join('data', 'priority.json')
PRIORITY_D: dict

with open(PRIORITY_PATH) as f:
    PRIORITY_D = json.load(f)

class Section:
    """Represents a section of a course, with course code, section
    number (and campus if applicable), and meeting days and times.
    """
    def __init__(self, course, section, days, times) -> None:
        self.course = course        # str
        self.section = section      # str
        self.days = days            # list[str]
        self.start_time: time = times[0]    # time
        self.end_time: time = times[1]      # time
    
    def __repr__(self):
        if len(self.section) < 3:
            return "HM-".join([self.course, self.section])
        else:
            return self.course + self.section[0:2] + '-' + self.section[2:4]
    
    def is_mandatory(self):
        # placeholder hard-code
        return PRIORITY_D[self.course] == 0
    
    def conflicts_with(self, other) -> bool:
        """
        Returns true if the calling section conflicts with the schedule
        """
        pass
        if type(other) == Section:
            # first check days
            sameDay = False
            for selfDay in self.days:
                for otherDay in other.days:
                    if selfDay == otherDay:
                        sameDay = True
                        break
                if sameDay:
                    break
            if not sameDay:
                return False
            
            # then times
            if (self.start_time >= other.start_time
                and self.start_time <= other.end_time):
                return True
            if (other.start_time >= self.start_time
                and other.start_time <= self.end_time):
                return True
            return False
        
        elif type(other) == Schedule:
            for section in other.sections:
                if self.conflicts_with(section):
                    return True
            return False
        
        else:
            raise TypeError("Argument was not a Section or a Schedule but a "
                            + str(type(other)))
        
    def to_dictionary(self) -> dict:
        """helper function for JSON"""
        # make time interpretable as JSON array
        start_time = [self.start_time.hour, self.start_time.minute]
        end_time = [self.end_time.hour, self.end_time.minute]
        # make properties interpretable as JSON
        d = {'course' : self.course,
             'section' : self.section,
             'days' : self.days,
             'start time' : start_time,
             'end time' : end_time}
        return d

    def toJSON(self, f: None | TextIOWrapper = None):
        """
        Creates a JSON object from a section object and returns it or
        writes it to the opened file object f, if given.
        """
        s = json.dumps(self.to_dictionary(), indent=2)
        if f:
            f.write(s)
        else:
            return s
    
    @classmethod
    def fromJSON(cls, src: TextIOWrapper | str):
        """Returns a section object from a json object"""
        # convert to string if necessary and then turn into dictionary
        if type(src) == TextIOWrapper:
            src = src.read()
        d = json.loads(src)
        # recover times as time objects
        start_time = d['start time']
        start_time = time(start_time[0], start_time[1])
        end_time = d['end time']
        end_time = time(end_time[0], end_time[1])
        # instantiate object and return
        args = [d['course'], d['section'], d['days'], [start_time, end_time]]
        return cls(*args)


class Schedule:
    """
    Represents a class schedule, with a list of sections,
    a prioritization score, and start and end times
    """
    def __init__(self, sections=[], score=0,
                 start_time=None, end_time=None):
        self.sections: list[Section] = sections
        self.score: float = score
        self.start_time: time = start_time
        self.end_time: time = end_time
        for section in sections:
            self.add(section, inplace=True)

    def __repr__(self, rich=False):
        s = ''
        s += 'Schedule with score {:.2f}, start time {}, and end time {}\n' \
               .format(self.score, self.start_time.isoformat('minutes'),
                       self.end_time.isoformat('minutes'))
        if rich:
            for section in self.sections:
                s += (str(section) + ' ' + ''.join(section.days) + ' '
                      + section.start_time.isoformat('minutes')
                      + ' - ' + section.end_time.isoformat('minutes') + '\n')
        return s[:-1] # remove the last newline
    
    def richSummary(self):
        return self.__repr__(rich=True)

    def copy(self):
        """Returns a copy of the schedule"""
        return Schedule(self.sections.copy(), self.score,
                        self.start_time, self.end_time)
    
    def add(self, section: Section, *, inplace=False):
        """Adds a section to the schedule"""
        if inplace:
            schedule = self
        else:
            schedule = self.copy()
            if section not in schedule.sections:
                schedule.sections.append(section)
                if not schedule.start_time:
                    schedule.start_time = section.start_time
                    schedule.end_time = section.end_time
                else:
                    schedule.start_time = min(schedule.start_time, section.start_time)
                    schedule.end_time = max(schedule.end_time, section.end_time)
                schedule.updateScore()
        return schedule

    def remove(self, code, *, inplace=False):
        pass

    def updateScore(self):
        """Updates the prioritazation score"""
        self.score = 0
        for section in self.sections:
            if PRIORITY_D[section.course] != 0:
                self.score += float(1 / PRIORITY_D[section.course])
    
    def to_dictionary(self) -> dict:
        """helper function for JSON"""
        # make time interpretable as JSON array
        start_time = [self.start_time.hour, self.start_time.minute]
        end_time = [self.end_time.hour, self.end_time.minute]
        # make properties interpretable as JSON
        d = {'sections' : [section.to_dictionary()
                           for section in self.sections],
             'score' : self.score,
             'start time' : start_time,
             'end time' : end_time}
        return d

    def toJSON(self, f: None | TextIOWrapper = None):
        """
        Creates a JSON object from a schedule object and returns it or
        writes it to the opened file object f, if given.
        """
        s = json.dumps(self.to_dictionary(), indent=2)
        if f:
            f.write(s)
        else:
            return s
    
    @classmethod
    def fromJSON(cls, src: TextIOWrapper | str):
        """Returns a schedule object from a json object."""
        # convert to string if necessary and then turn into dictionary
        if type(src) == TextIOWrapper:
            src = src.read()
        # TODO: unpack sections from JSON
        d = json.loads(src)
        d['sections'] = [Section.fromJSON(jsonSection)
                         for jsonSection in d['sections']]
        # recover times as time objects
        start_time = d['start time']
        start_time = time(start_time[0], start_time[1])
        end_time = d['end time']
        end_time = time(end_time[0], end_time[1])
        # instantiate object and return
        args = [d['sections'], d['score'], start_time, end_time]
        return cls(*args)
