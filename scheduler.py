from dataTypes import Schedule, Section
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
    sections: dict[str, list[Section]] = {}
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
    if coursesToAdd == []:          # bottom of recursion
        return [existingSchedule]
    
    # each subtree includes one of the sections of that course
    newSchedules = []
    for section in coursesToAdd[0]: # from the current course group to add
        if not section.conflictsWith(existingSchedule):
            # add to the list all of the schedules that can be made by
            # including that section
            # this relies on add not being in place
            newSchedules += makeSchedules(existingSchedule.add(section),
                                          coursesToAdd[1:])
    # we also consider not adding the course at all, unless mandatory
    if not section.isMandatory():
        newSchedules += makeSchedules(existingSchedule, coursesToAdd[1:])
    # now we have reached the end of the recursion and newSchedules has
    # every possible schedule
    return newSchedules


def getSortedSchedules() -> list[Schedule]:
    """
    Facilitates the generation of schedules by getting sections from
    courseData.txt and then wrapping the recursive makeSchedules with
    starter parameters
    """
    # get sections from text file
    with open('data/courseData.txt', 'r') as f:
        sections = list(readSections(f).values())
    # start off the recursive schedule generation
    blankSchedule = Schedule()
    schedules = makeSchedules(blankSchedule, sections)
    # remove empty schedules and sort them by score
    schedules = list(filter(lambda x : len(x.sections) > 0, schedules))
    schedules.sort(key = lambda sched : sched.score, reverse = True)
    return schedules


def writeJSON():
    import json
    schedules = getSortedSchedules()
    with open('data/sortedSchedules.json', 'w') as f:
        json.dump([schedule.toDictionary() for schedule in schedules], f)

if __name__ == "__main__":
    # import sys
    # if len(sys.argv) > 0 and sys.argv[1] == 'write':
    writeJSON()
