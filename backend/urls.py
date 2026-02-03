from django.urls import path
from django.contrib import admin

from .views import (
    login_view,
    dashboard_view,
    attendance_view,
    logout_view
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", login_view, name="login"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("", dashboard_view, name="dashboard"),
    path("attendance/", attendance_view, name="attendance"),
    path("logout/", logout_view, name="logout"),
]
