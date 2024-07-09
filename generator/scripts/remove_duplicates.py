from ..models import User, Schedule

def remove_duplicate_schedules_by_user(user: User):
    Schedule.remove_duplicates(user)

def remove_duplicate_schedules():
    for user in User.objects.all():
        remove_duplicate_schedules_by_user(user)

if __name__ == "__main__":
    remove_duplicate_schedules()