Contains the data that comes in and out or is intermediately used

IN:
courseData.txt
The data for courses and sections. I want to replace the existence of this
file with communication with a front end, and then JSON to store it instead
of my specific text format.

priorities.txt
The python dictionary with priorities. I also want to replace this with
a frontend input and then JSON storage.


INTERMEDIATE:
sortedSchedules.json
The sorted list of schedules, which is hopefully only generated one time, or
maybe regenerated whenever the user thinks of new courses/sections they may
want. Most of the utility then comes from filtering and browsing this list.
