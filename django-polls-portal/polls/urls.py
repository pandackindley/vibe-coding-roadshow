from django.urls import path

from polls import views

urlpatterns = [
    path("", views.poll_list, name="poll_list"),
    path("create/", views.create_poll_page, name="create_poll_page"),
    path("<uuid:poll_id>/respond/", views.respond_poll_page, name="respond_poll_page"),
    path("<uuid:poll_id>/results/", views.results_page, name="results_page"),
    path("<uuid:poll_id>/review/", views.review_poll_page, name="review_poll_page"),
]
