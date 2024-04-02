from dataTypes import *
from io import TextIOWrapper

def readSections(f: TextIOWrapper) -> list[CourseSection]:
    """
    Turn text data into a list of CourseSection objects
    Text format:
    course
        section days startTime-endTime
    Example:
    CSCI070
        01 MW 0935-1050
        02 MW 1100-1215
        03 MW 1445-1600
    """
    sections = []
    line = f.readline()
    while line != "":   # otherwise EOF
        if line != '\n':    # otherwise empty line
            if line[0] != ' ':  # course title with no indent
                course = line.strip()
            else:   # indented section line under course line
                sectionData = line.split()
                section = sectionData[0]
                days = [day for day in sectionData[1]]
                time = [sectionData[2][:4], sectionData[2][5:9]]
                sections.append(CourseSection(course, section, days, time))
        line = f.readline()
    return sections

def getScore(schedule: Schedule) -> int:
    """
    Return a score indicating how well a course aligns with priorities
    """
    pass

def makeSchedules(sections: list[CourseSection], length) -> list[Schedule]:
    """
    Make a list of schedules that contain each course no more than one time.
    Each schedule must include sections of required courses.
    """
    # build around mandatory courses, i.e. first add mandatory courses
    pass

def main():
    """
    For testing
    """
    f = open('courseData.txt', 'r')
    print(readSections(f))
    f.close()

main()