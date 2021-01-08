from django.urls import path
from . import views


urlpatterns = [
    path('', views.JobListCreateAPIView.as_view(), name="list_create_jobs"),
    path('<int:job_id>', views.RetrieveUpdateDestroyJobAPIView.as_view(), name="retrieve_update_destroy_job"),
    path('<int:job_id>/proposals', views.ListCreateProposal.as_view(), name="list_create_proposal"),
    path('/proposals/<int:proposal_id>', views.RetrieveUpdateDestroyProposal.as_view(), name="retrieve_update_destroy_proposal"),
    path('<int:job_id>/save', views.save_job, name="save_job"),
    path('<int:job_id>/unsave', views.unsave_job, name="unsave_job"),

]
