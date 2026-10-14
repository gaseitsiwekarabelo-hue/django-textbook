"""
URL configuration for my_first_project project.
"""

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # Django administration.
    path("admin/", admin.site.urls),

    # Hello World application.
    path("hello/", include("hello_world.urls")),

    # Library application.
    path("library/", include("library.urls")),
]