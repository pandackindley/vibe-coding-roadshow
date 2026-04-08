from django.urls import path

from polls.api import views

urlpatterns = [
    path("polls", views.CreatePollView.as_view(), name="api_create_poll"),
    path("polls/<uuid:poll_id>/publish", views.PublishPollView.as_view(), name="api_publish_poll"),
    path("polls/<uuid:poll_id>/responses", views.SubmitResponseView.as_view(), name="api_submit_response"),
    path("polls/<uuid:poll_id>/results", views.ResultsView.as_view(), name="api_poll_results"),
    path("polls/<uuid:poll_id>/reviews", views.ReviewView.as_view(), name="api_poll_reviews"),
]
