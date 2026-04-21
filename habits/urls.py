from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_habit, name='add_habit'),
    path('delete/<int:habit_id>/', views.delete_habit, name='delete_habit'),
    path('log/<int:habit_id>/', views.log_habit, name='log_habit'),
    path('signup/', views.signup, name='signup'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]