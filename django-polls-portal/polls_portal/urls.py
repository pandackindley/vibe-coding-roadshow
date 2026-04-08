from django.contrib import admin
from django.urls import include, path

from polls import views as web_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", web_views.home, name="home"),
    path("polls/", include("polls.urls")),
    path("api/", include("polls.api.urls")),
]
