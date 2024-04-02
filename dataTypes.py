class Schedule:
    pass

class CourseSection:
    def __init__(self, course, section, days, time) -> None:
        self.course = course
        self.section = section
        self.days = days
        self.startTime = time[0]
        self.endTime = time[1]
    
    def __repr__(self):
        return "-".join([self.course, self.section])
    
    def isMandatory(self):
        # placeholder hard-code
        return self.course in ('ENGR079', 'ENGR079P')
    
    def conflictsWith(self, other) -> bool:
        """
        Returns true if the two classes have conflicting times
        """
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
        selfStart, selfEnd, otherStart, otherEnd = \
            map(int,
                [self.startTime, self.endTime,
                 other.startTime, other.endTime]
                )
        return (
            selfStart in range(otherStart, otherEnd)
            or selfEnd in range(otherStart, otherEnd)
        )
    
    def isDuplicate(self, other) -> bool:
        return self.course == other.course