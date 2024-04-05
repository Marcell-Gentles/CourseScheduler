# 5C Automatic Course Scheduler

This tool (in progress) finds schedules for you based on the courses you want to take, and how important they are to you. At this time, you have to provide the following data in the specified format to `courseData.txt`:
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
    01 MW 0935-1050
    02 MW 1100-1215
    03 MW 1445-1600

MATH055
    CM01 TR 1100-1215
    01 MW 1315-1430
    02 MW 1445-1600
    03 TR 1315-1430
    PZ01 TR 0810-0925
    PZ02 TR 0935-1050
```

In `dataTypes.py` is a dictionary `PRIORITY_D` where you can set the priority of each course. 0 indicates that the course is mandatory (and no schedule without it will be generated), 1 is highly desired, etc.

As of this commit, there is functionality to generate the list of all possible schedules, sorted by prioritization score (where a higher score is better). In the future, I plan to add prioritization at the section level, so you can prefer a certain professor or even campus.

I plan to add the following features before course registration day (April 18, 2024 for me, a freshman).

### Browsing
Paginated browsing of sorted schedules with informative summaries of variable levels of detail

### Filtering
* Time (start of first class, end of last)
* Prioritization score
* Courses included/excluded
    * Filter includes mandatory courses by default
* Individual sections
    * Included (say I want to be in my friend’s class)
    * Excluded (a section fills up)
        * Persistent exclusion list for keeping track of full sections during registration


## Future
As soon as possible, I would like to improve the UI. The way I have required the course data be provided is not great, and the browsing should be smooth. First I will improve the terminal-based experience then maybe build an HTML / JS interface.

Long-term, I hope to be able to add this functionality to [HyperSchedule](https://github.com/hyperschedule/hyperschedule) for the following reasons.

* **Ease of data importation**: The user wouldn't have to manually import the course section data—hyperschedule already has it and all the user would have to provide would be courses and priorities.

* **Automatic section exclusion**: Once a section fills up, Hyperschedule could automatically filter out all of the schedules that include that section, without the user having to try to add that section, only to find that it is full and then frantically provide that information and 

Also, Hyperschedule is far better as a course browser than Harvey Mudd's portal, and this feature would make it even better. I am a big fan of having one application that does everything you want it to instead of several that depend on one another.


## Implementation Roadmap
1. Section and Schedule classes
    1. methods to export to JSON and import from JSON
2. schedule generator
3. Design and implement scoring
4. Filtering predicate generators
5. Browser
6. Persistent filtering (section exclusion)

As of this commit, 1.1, 4, 5, and 6 remain.