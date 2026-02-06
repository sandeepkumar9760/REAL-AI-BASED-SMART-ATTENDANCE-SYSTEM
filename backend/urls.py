from django.contrib import admin
from django.urls import path
from .views import (
    login_view,
    dashboard_view,
    attendance_view,
    logout_view,
    get_students,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", login_view, name="login"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    path("dashboard/", dashboard_view, name="dashboard"),
    path("attendance/", attendance_view, name="attendance"),

    # AJAX
    path("get-students/", get_students, name="get_students"),
]
