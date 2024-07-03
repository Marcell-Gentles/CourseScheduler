from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .businesslogic.score_generate import make_schedules, score

# Create your views here.

def generate_schedules(request: HttpRequest):
    # TODO: make sure a user has entered priorities (or set mandatory)
    # before proceeding
    make_schedules(request.user)
    return HttpResponse("Schedules created")


# form where the user enters Courses (creating them and Departments if needed)
# and their priorities on them (CoursePriority)
def set_priorities(request: HttpRequest):
    if request.method == 'GET':
        # deliver page ...
        # on the page the user starts typing the
        # full course representation and it autocompletes
        # if it exists
        # when they submit the course it is validated and added
        # to the database, and they set their priority level for it
        pass
    if request.method == 'POST':
        pass
    pass

def browse_schedules(request):
    # schedule browser sorted by score
    pass

# show a graphical view of the schedule and its data (score!)
def view_schedule(request):
    pass
