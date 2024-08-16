# Automatic Course Scheduler

This tool finds schedules for you based on the courses you want to take, and how important they are to you. It builds every possible schedule that inlcudes one section of each of the mandatory coures, as well as one section of zero or more other courses of interst. Each schedule gets a score based on the courses it includes. This score is determined from the priorities you provide for each course. You can view and filter schedules in the browser. See [`manual.md`](manual.md).

<img width="900" alt="course-scheduler-demo" src="https://github.com/user-attachments/assets/6af9fb5d-0e18-4a11-9160-4dc9d421407c">

## Future

I plan to improve the user experience for inputting section and course information, and to provide a web interface for browsing and filtering sorted schedules.

Long-term, I hope to be able to add this functionality to [HyperSchedule](https://github.com/hyperschedule/hyperschedule) for the following reasons.

* **Ease of data importation**: The user wouldn't have to manually import the course section data—hyperschedule already has it and all the user would have to provide would be courses and priorities.

* **Automatic section exclusion**: Once a section fills up, Hyperschedule could automatically filter out all of the schedules that include that section, without the user having to try to add that section, only to find that it is full and then frantically provide that information and repeat the same process for any new sections they find have filled up.

Also, Hyperschedule is far better as a course browser than Mudd's portal, and this feature would make it even better. I am a big fan of having one application that does everything you want it to instead of several that depend on one another.
