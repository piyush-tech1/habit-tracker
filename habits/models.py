from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        unique_together = ['habit', 'date']