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
In the "sections" field is an array of course objects.

Schedule:
{
    "sections": [
        <sections>
    ],
    "score": <score>,
    "start time": [
        <hour>,
        <minute>
    ],
    "end time": [
        <hour>,
        <minute>
    ]
}

Section:
{
    "course": <course code>,
    "section": <section campus/number>,
    "days": [
        <days>
    ],
    "start time": [
        <hour>,
        <minute>
    ],
    "end time": [
        <hour>,
        <minute>
    ]
}

The following is an example schedule. sorted_schedules.json should contain
an array of these.

{
  "sections": [
    {
      "course": "ENGR079",
      "section": "07",
      "days": [
        "M",
        "W"
      ],
      "start time": [
        11,
        0
      ],
      "end time": [
        11,
        50
      ]
    },
    {
      "course": "ENGR079P",
      "section": "08",
      "days": [
        "F"
      ],
      "start time": [
        15,
        0
      ],
      "end time": [
        17,
        30
      ]
    }
  ],
  "score": 0,
  "start time": [
    11,
    0
  ],
  "end time": [
    17,
    30
  ]
}