from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Schedule
from .forms import *


# Create your views here.

@login_required
def generate_schedules(request: HttpRequest):
    # TODO: make sure a user has entered priorities (or set mandatory)
    # before proceeding
    first_time: bool = request.user.schedule_set.count() == 0
    Schedule.generate(request.user)
    schedule_count = request.user.schedule_set.count()
    response = (f"You created {schedule_count} schedules" if first_time
                else f"You have {schedule_count} schedules")
    return HttpResponse(response)

@login_required
def set_priorities(request: HttpRequest):
    if request.method == 'GET':
        edit = False
        if 'edit' in request.GET:
            edit = True
            pk = request.GET['pk']
            form = PriorityForm(
                instance=CoursePriority.objects.get(pk=pk)
            )
        else:
            form = PriorityForm()
        user = request.user
        priorities = user.coursepriority_set.all()
        # if priorities:      # the user has existing preferences
        context = {
            "priorities": priorities,
            "form": form,
            "edit": edit
        }
        return render(request, "generator/priorities.html", context)

    if request.method == 'POST':
        form = PriorityForm(request.POST)
        if form.is_valid():
            form_priority: CoursePriority = form.save(commit=False)
            # could be an edit or new
            db_priority: CoursePriority = CoursePriority.objects.get_or_create(
                user=request.user, course=form_priority.course
            )
            db_priority.level = form_priority.level
            db_priority.mandatory = form_priority.mandatory
            db_priority.save()
            # the base priorities URL
            return HttpResponseRedirect(request.path_info)
        else:
            context = {
                "priorities": request.user.coursepriority_set.all(),
                "form": form,
                "edit": True
            }
            return render(request, "generator/priorities.html", context)


def browse_schedules(request):
    # schedule browser sorted by score
    pass

# show a graphical view of the schedule and its data (score!)
def view_schedule(request):
    pass
