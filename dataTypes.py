from datetime import time

# 0 for mandatory. The lowest numbers are weighted way more
PRIORITY_D = {'ENGR079' : 0,
              'ENGR079P' : 0,
              'MATH055' : 1,
              'CSCI070' : 1,
              'LGCS010' : 2,
              'MATH056' : 3,
              'PHYS050' : 4,
              'ENGR085' : 5}

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

    # def conflictsWith(self, section: Section):
    #     """Alternate way to check for conflicts"""
    #     return section.conflictsWith(self)

class Section:
    """
    Represents a section of a course, with course code, section number
    (and campus if applicable), and meeting days and times
    """
    def __init__(self, course, section, days, time) -> None:
        self.course = course        # str
        self.section = section      # str
        self.days = days            # list[str]
        self.startTime = time[0]    # time
        self.endTime = time[1]      # time
    
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
