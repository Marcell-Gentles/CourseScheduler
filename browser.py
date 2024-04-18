from datatypes import Schedule
from scheduler import get_sorted_schedules
from filter import Filterer
import time


PAGE_SIZE = 6

def make_page(schedules: list[Schedule], start, size=PAGE_SIZE):
    """Returns a page of size number of schedules starting at index
    start in the list"""
    s = ''
    for i, schedule in enumerate(schedules[start:start+size]):
        s += f'#{i+start}\n'
        s += str(schedule) + '\n' + schedule.summarize_daily() +'\n'
    return s

def get_schedule(schedules: list[Schedule], number: int):
    """Returns the details needed to find the sections from the section number
    in the portal.
    """
    schedule = schedules[number]
    s = ''
    for section in schedule.sections:
        s += section.course + ' ' + section.section + '\n'
    return s

def main():
    schedules = get_sorted_schedules()
    f = Filterer()

    print('There are', len(schedules), 'schedules.')
    optimal_schedules = [schedule for schedule in schedules
               if schedule.score == schedules[0].score]
    print(len(optimal_schedules), 'of them are optimal.')

    options_dialog = ("Type q to quit, n to see the next page, p to see the "
                      "previous page, f to edit filters.\n"
                      "Type the number of a schedule to show its details.\n")
    
    print("You are now entering the browser.")
    time.sleep(2)

    page_start = 0
    while True:
        filtered_schedules = list(filter(f.filter, schedules))
        print()
        print(make_page(filtered_schedules, page_start))
        if f.filters:
            print("Active filters" + '\n' + str(f) + '\n')
        else:
            print("No active filters\n")
        print(options_dialog)
        inp = input()
        print()

        if inp == 'q':
            break
        elif inp == 'n':
            print("Going to next page")
            time.sleep(1)
            page_start += PAGE_SIZE
            continue
        elif inp == 'p':
            print("Going to previous page")
            time.sleep(1)
            page_start -= PAGE_SIZE
            continue
        
        elif inp.isnumeric():
            try:
                inp = int(inp)
                print(f'Schedule #{inp}:')
                print(get_schedule(filtered_schedules, inp))
                print()
                input("Enter any value to return to the browser")
                continue
            except:
                print("Invalid number")
                time.sleep(1)
                continue
        
        elif inp == 'f':
            print("Would you like to add a filter, remove a filter, or clear "
                  "all filters? (enter add, rem, or clr)")
            inp = input()
            print()
            if inp == 'add':
                kind = input(
                    "What kind of filter would you like to add?\n"
                    "time: earliest start and/or latest end time\n"
                    "score: minimum score\n"
                    "courses_I: courses that must be included\n"
                    "courses_X: courses that must be excluded\n"
                    "sections_I: sections that must be included\n"
                    "sections_X: sections that must be excluded\n"
                    "\n"
                )
                if kind == 'score':
                    score = float(input("Enter the minimum score: "))
                    f.add('score', [score])

                elif kind == 'time':
                    start = input("Enter the start time "
                                  "(24H HHMM format, blank if none): ")
                    end = input("Enter the end time: ")
                    if not start:
                        start = None
                    if not end:
                        end = None
                    f.add('time', [], {'start': start, 'end': end})

                elif kind in ('courses_I', 'courses_X'):
                    print("Enter one course at a time then "
                          "enter a blank when done")
                    args = []
                    while True:
                        inp = input()
                        if inp == '':
                            break
                        else:
                            args += [inp]
                    f.add(kind, args)

                elif kind in ('sections_I', 'sections_X'):
                    print("Enter the following information for one section "
                          "at a time. Enter a blank for course code "
                          "when done.")
                    args = []
                    while True:
                        course = input("Course code: ")
                        if course == '':
                            break
                        else:
                            section = input("Section code: ")
                            args += [course, section]
                    f.add(kind, args)

                else:
                    print("Invalid filter operation")
                    time.sleep(1)
                    continue

            elif inp == 'rem':
                print("Active filters:")
                print(f)
                inp = input("Enter the number of the filter to remove: ")
                f.remove(int(inp))

            elif inp == 'clr':
                conf = input("Enter 'y' if you are sure you want "
                             "to clear all filters: ")
                if conf.lower() == 'y':
                    f.reset()

            else:
                print("Invalid filter operation")
                time.sleep(1)
            
            continue
        
        else:
            print("Invalid choice")
            time.sleep(1)
            continue

main()