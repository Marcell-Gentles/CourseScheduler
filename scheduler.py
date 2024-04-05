from dataTypes import *
from io import TextIOWrapper
import datetime

def readSections(f: TextIOWrapper) -> dict[str, list[Section]]:
    """
    Turn text data into a dictionary of lists of Sections of the same course
    keyed by their code
    Text format:
    course
        section days startTime-endTime
    Example:
    CSCI070
        01 MW 0935-1050
        02 MW 1100-1215
        03 MW 1445-1600
    """
    sections = {}
    line = f.readline()
    while line != "":   # otherwise EOF
        if line != '\n':    # otherwise empty line
            if line[0] != ' ':  # course title with no indent
                course = line.strip()
                sections[course] = []
            else:   # indented section line under course line
                sectionData = line.split()
                section = sectionData[0]
                days = [day for day in sectionData[1]]
                # turn the string times into time objects
                startTime = sectionData[2][:4]
                startTime = datetime.time(int(startTime[0:2]), int(startTime[2:4]))
                endTime = sectionData[2][5:9]
                endTime = datetime.time(int(endTime[0:2]), int(endTime[2:4]))
                time = [startTime, endTime]
                sections[course].append(Section(course, section, days, time))
        line = f.readline()
    return sections

def makeSchedules(existingSchedule: Schedule,
                  coursesToAdd: list[list[Section]]) -> list[Schedule]:
    """
    Make a list of schedules that contain each course no more than one time.
    No schedule will be made that does not include the mandatory courses.
    """
    if coursesToAdd == []:
        return [existingSchedule]
    
    newSchedules = []
    for section in coursesToAdd[0]: # from the current course group to add
        if not section.conflictsWith(existingSchedule):
            newSchedules += makeSchedules(existingSchedule.add(section),
                                          coursesToAdd[1:])
    # we also consider not adding the course, unless mandatory
    if not section.isMandatory():
        newSchedules += makeSchedules(existingSchedule, coursesToAdd[1:])
    return newSchedules

def getSortedSchedules():
    f = open('courseData.txt', 'r')
    sections = list(readSections(f).values())
    f.close()

    blankSchedule = Schedule()
    schedules = makeSchedules(blankSchedule, sections)
    schedules.sort(key = lambda sched : sched.score, reverse = True)

    return schedules

def main():
    schedules = getSortedSchedules()
    perfectScore = schedules[0].score
    print("Number of perfect schedules: {}\n".format(len([schedule for schedule in schedules
                                                        if schedule.score == perfectScore])))
    for schedule in getSortedSchedules()[:100]:
        print(schedule.richSummary())
        print()
    

main()