from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListFreelancers.as_view(), name="list_frelancers"),
    path('<str:username>', views.UserProfileDetail, name="profile_detail"),
    path("<str:username>/config", views.UpdateProfileView, name="update_profile"),
    path('become_freelancer/', views.become_freelancer, name="become_freelancer"),
    path('un_become_freelancer/', views.un_become_freelancer, name="un_become_freelancer"),
    path('skills/', views.ListSkills.as_view(), name="list_skills"),
]
