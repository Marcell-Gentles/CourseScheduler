# User Manual

## Adding Your Data

### Adding Courses and Sections

Fill `data/course_data.txt` with your course and section data in the following format:

```
COURSE_CODE
    SECTION_NUMBER DAYS TIME
    SECTION_NUMBER DAYS TIME
    ...

COURSE_CODE
    SECTION_NUMBER DAYS TIME
    ...

...

```

For example:
```
CSCI070
    01HM MW 0935-1050
    02HM MW 1100-1215
    03HM MW 1445-1600

MATH055
    CM01 TR 1100-1215
    01HM MW 1315-1430
    02HM MW 1445-1600
    03HM TR 1315-1430
    PZ01 TR 0810-0925
    PZ02 TR 0935-1050
```

The way you write the course codes (e.g. CS70 vs CSCI070) is not
critical to the functioning of this program, but it is important to stay
consistent, because that is how you will need to refer to that course whenever
you want to filter with it or want to search for it in the future, and that
is how that course will be represented when you are presented a schedule from
the list that is made.

For the other information, it is crucial that you follow this format, with the
following data seperated with spaces following 4 spaces of indentation before
the first item:
1. the two digit section code followed by the two letter campus code
2. the day of the week abbreviations (MTWRF) capitalized, following that
abbreviation system, and placed next to each other without spaces
3. the start and end times of the section, written in 24-hour format with no
colon separating the hour and minute (1100 vs. 11:00), and a single hyphen
separating the start and end times

### Adding Priorities

The scheduler scores schedules by how well they accommodate your course
priorities. This requires that you give each course you added to
`data/course.data.txt` a priority level in `data/priority.json` using this
scheme:
* 0 for courses that you absolutely **must** have in your schedule. No
schedule without these courses will be generated.
* 1 for the remaining courses(s) of highest priority and 2, 3, 4, etc for ones
that are less important to you.

This following example demonstrates the format:

```
{
  "ENGR079": 0,
  "ENGR079P": 0,
  "MATH055": 1,
  "CSCI070": 1
}
```

The course names given here must match those in `course_data.txt`.
Note that you can have multiple courses at the same priority level.


## Browsing Schedules

Run `browser.py`.