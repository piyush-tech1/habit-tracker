from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from .models import Habit, HabitLog
from .forms import HabitForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def signup(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form=UserCreationForm()
    return render(request,'registration/signup.html',{'form':form})


@login_required
def log_habit(request, habit_id):
    habit=Habit.objects.get(id=habit_id)
    today=date.today()
    HabitLog.objects.get_or_create(habit=habit, date=today)
    return redirect('dashboard')

@login_required
def delete_habit(request, habit_id):
    habit=Habit.objects.get(id=habit_id)
    habit.delete()
    return redirect('dashboard')

@login_required
def add_habit(request):
    if request.method == 'POST':
        form=HabitForm(request.POST)
        if form.is_valid():
            habit=form.save(commit=False)
            habit.user=request.user
            habit.save()
            return redirect('dashboard')
    else:
        form=HabitForm()
        return render(request, "habits/habit_add.html", {'form': form})


@login_required
def get_streak(habit):
    today = date.today()
    streak = 0
    current_date = today

    while True:
        logged=HabitLog.objects.filter(habit=habit,date=current_date).exists()
        if logged:
            streak +=1
            current_date -= timedelta(days=1)
        else:
            break

    return streak

@login_required
def dashboard(request):
    habits = Habit.objects.filter(user=request.user)
    today = date.today()

    # For each habit check if already logged today
    habits_with_status=[]
    for habit in habits:
        already_logged = HabitLog.objects.filter(habit=habit, date=today).exists()
        habits_with_status.append({
            'habit': habit,
            'logged_today': already_logged,
            'streak': get_streak(habit),
        })

    total=habits.count()
    complete_today=sum(1 for h in habits_with_status if h ['logged_today'])

    return render(request, 'habits/dashboard.html',{
        'habits': habits_with_status,
        'total': total,
        'completed_today': complete_today,
        'today': today,
    })
    