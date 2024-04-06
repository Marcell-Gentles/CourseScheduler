from datatypes import Schedule, Section
from io import TextIOWrapper
import datetime
import os


JSON_WRITE_PATH = os.path.join('data', 'sorted_schedules.json')
COURSE_DATA_PATH = os.path.join('data', 'course_data.txt')


def read_sections(f: TextIOWrapper) -> dict[str, list[Section]]:
    """Turns text data into a dictionary of lists of Sections of the
    same course keyed by their code.
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
                section_data = line.split()
                section = section_data[0]
                days = [day for day in section_data[1]]
                # turn the string times into time objects
                start_time = section_data[2][:4]
                start_time = datetime.time(int(start_time[0:2]),
                                           int(start_time[2:4]))
                end_time = section_data[2][5:9]
                end_time = datetime.time(int(end_time[0:2]),
                                         int(end_time[2:4]))
                time = [start_time, end_time]
                sections[course].append(Section(course, section, days, time))

        line = f.readline()
    return sections


def make_schedules(existing_schedule: Schedule,
                  courses_to_add: list[list[Section]]) -> list[Schedule]:
    """Makes a list of schedules that contain each course no more than
    one time. No schedule will be made that does not include the
    mandatory courses.
    """
    if courses_to_add == []:          # bottom of recursion
        return [existing_schedule]
    
    # each subtree includes one of the sections of that course
    new_schedules = []
    for section in courses_to_add[0]: # from the current course group to add
        if not section.conflicts_with(existing_schedule):
            # add to the list all of the schedules that can be made by
            # including that section
            # this relies on add not being in place
            new_schedules += make_schedules(existing_schedule.add(section),
                                            courses_to_add[1:])
    # we also consider not adding the course at all, unless mandatory
    if not section.is_mandatory():
        new_schedules += make_schedules(existing_schedule, courses_to_add[1:])
    # now we have reached the end of the recursion and newSchedules has
    # every possible schedule
    return new_schedules


def get_sorted_schedules() -> list[Schedule]:
    """Facilitates the generation of schedules by getting sections from
    courseData.txt and then wrapping the recursive makeSchedules with
    starter parameters
    """
    # get sections from text file
    with open(COURSE_DATA_PATH, 'r') as f:
        sections = list(read_sections(f).values())
    # start off the recursive schedule generation
    blank_schedule = Schedule()
    schedules = make_schedules(blank_schedule, sections)
    # remove empty schedules and sort them by score
    schedules = list(filter(lambda x: len(x.sections) > 0, schedules))
    schedules.sort(key = lambda sched: sched.score, reverse = True)
    return schedules


def writeJSON():
    import json
    schedules = get_sorted_schedules()
    with open(JSON_WRITE_PATH, 'w') as f:
        json.dump([schedule.to_dictionary() for schedule in schedules], f)

if __name__ == "__main__":
    # import sys
    # if len(sys.argv) > 0 and sys.argv[1] == 'write':
    writeJSON()
