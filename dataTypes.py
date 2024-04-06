from datetime import time
from priorities import PRIORITY_D
import json
from io import TextIOWrapper

class Schedule:
    """
    Represents a class schedule, with a list of sections,
    a prioritization score, and start and end times
    """
    def __init__(self, sections=[], score=0,
                 startTime=None, endTime=None):
        self.sections: list[Section] = sections
        self.score: float = score
        self.startTime: time = startTime
        self.endTime: time = endTime
        for section in sections:
            self.add(section, inplace=True)

    def __repr__(self, rich=False):
        s = ''
        s += 'Schedule with score {:.2f}, start time {}, and end time {}\n' \
        .format(self.score, self.startTime.isoformat('minutes'),
                self.endTime.isoformat('minutes'))
        if rich:
            for section in self.sections:
                s += str(section) + ' ' + ''.join(section.days) + ' ' \
                    + section.startTime.isoformat('minutes') \
                        + ' - ' + section.endTime.isoformat('minutes') + '\n'
        return s[:-1] # remove the last newline
    
    def richSummary(self):
        return self.__repr__(rich=True)

    def copy(self):
        """Returns a copy of the schedule"""
        return Schedule(self.sections.copy(), self.score,
                        self.startTime, self.endTime)
    
    def add(self, section, *, inplace=False):
        """Adds a section to the schedule"""
        if inplace:
            schedule = self
        else:
            schedule = self.copy()
            if section not in schedule.sections:
                schedule.sections.append(section)
                if not schedule.startTime:
                    schedule.startTime = section.startTime
                    schedule.endTime = section.endTime
                else:
                    schedule.startTime = min(schedule.startTime, section.startTime)
                    schedule.endTime = max(schedule.endTime, section.endTime)
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
    
    def toDictionary(self) -> dict:
        """helper function for JSON"""
        # make time interpretable as JSON array
        startTime = [self.startTime.hour, self.startTime.minute]
        endTime = [self.endTime.hour, self.endTime.minute]
        # make properties interpretable as JSON
        d = {'sections' : [section.toDictionary()
                           for section in self.sections],
             'score' : self.score,
             'start time' : startTime,
             'end time' : endTime}
        return d

    def toJSON(self, f: None | TextIOWrapper = None):
        """
        Creates a JSON object from a schedule object and returns it or
        writes it to the opened file object f, if given.
        """
        s = json.dumps(self.toDictionary(), indent=2)
        if f:
            f.write(s)
        else:
            return s
    
    @classmethod
    def fromJSON(cls, src: TextIOWrapper | str):
        """Returns a schedule object from a json object"""
        # convert to string if necessary and then turn into dictionary
        if type(src) == TextIOWrapper:
            src = src.read()
        # TODO: unpack sections from JSON
        d = json.loads(src)
        d['sections'] = [Section.fromJSON(jsonSection)
                         for jsonSection in d['sections']]
        # recover times as time objects
        startTime = d['start time']
        startTime = time(startTime[0], startTime[1])
        endTime = d['end time']
        endTime = time(endTime[0], endTime[1])
        # instantiate object and return
        args = [d['sections'], d['score'], startTime, endTime]
        return cls(*args)



class Section:
    """
    Represents a section of a course, with course code, section number
    (and campus if applicable), and meeting days and times
    """
    def __init__(self, course, section, days, times) -> None:
        self.course = course        # str
        self.section = section      # str
        self.days = days            # list[str]
        self.startTime: time = times[0]    # time
        self.endTime: time = times[1]      # time
    
    def __repr__(self):
        if len(self.section) < 3:
            return "HM-".join([self.course, self.section])
        else:
            return self.course + self.section[0:2] + '-' + self.section[2:4]
    
    def isMandatory(self):
        # placeholder hard-code
        return PRIORITY_D[self.course] == 0
    
    def conflictsWith(self, other) -> bool:
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
            if self.startTime >= other.startTime \
                and self.startTime <= other.endTime:
                return True
            if other.startTime >= self.startTime \
                and other.startTime <= self.endTime:
                return True
            return False
        
        elif type(other) == Schedule:
            for section in other.sections:
                if self.conflictsWith(section):
                    return True
            return False
        
        else:
            raise TypeError("Argument was not a Section or a schedule but a "
                            + str(type(other)))
    
    def isRedundant(self, schedule: Schedule) -> bool:
        return self.course in [sec.course for sec in schedule.sections]
    
    def toDictionary(self) -> dict:
        """helper function for JSON"""
        # make time interpretable as JSON array
        startTime = [self.startTime.hour, self.startTime.minute]
        endTime = [self.endTime.hour, self.endTime.minute]
        # make properties interpretable as JSON
        d = {'course' : self.course,
             'section' : self.section,
             'days' : self.days,
             'start time' : startTime,
             'end time' : endTime}
        return d

    def toJSON(self, f: None | TextIOWrapper = None):
        """
        Creates a JSON object from a section object and returns it or
        writes it to the opened file object f, if given.
        """
        s = json.dumps(self.toDictionary(), indent=2)
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
        startTime = d['start time']
        startTime = time(startTime[0], startTime[1])
        endTime = d['end time']
        endTime = time(endTime[0], endTime[1])
        # instantiate object and return
        args = [d['course'], d['section'], d['days'], [startTime, endTime]]
        return cls(*args)

