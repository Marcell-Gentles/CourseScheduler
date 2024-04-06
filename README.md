# 5C Automatic Course Scheduler

This tool (in progress) finds schedules for you based on the courses you want to take, and how important they are to you. At this time, you have to provide the following data in the specified format to `data/courseData.txt`:
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

In `data/priorities.py` is a dictionary where you can set the priority of each course. 0 indicates that the course is mandatory (and no schedule without it will be generated), 1 is highly desired, etc.

As of this commit, there is functionality to generate the list of all possible schedules, sorted by prioritization score (where a higher score is better). In the future, I plan to add prioritization at the section level, so you can prefer a certain professor or even campus.

There is filtering functionality so that you can filter by the earliest class start time, latest clast end time, minimum score, courses included or excluded, and sections included or excluded. These filters can be saved and reloaded.


### Front End

I plan to improve the user experience for inputting section and course information, and to provide paginated and filtered browsing of sorted schedules with informative summaries of variable levels of detail


## Future

Long-term, I hope to be able to add this functionality to [HyperSchedule](https://github.com/hyperschedule/hyperschedule) for the following reasons.

* **Ease of data importation**: The user wouldn't have to manually import the course section data—hyperschedule already has it and all the user would have to provide would be courses and priorities.

* **Automatic section exclusion**: Once a section fills up, Hyperschedule could automatically filter out all of the schedules that include that section, without the user having to try to add that section, only to find that it is full and then frantically provide that information and repeat the same process for any new sections they find have filled up.

Also, Hyperschedule is far better as a course browser than Mudd's portal, and this feature would make it even better. I am a big fan of having one application that does everything you want it to instead of several that depend on one another.
