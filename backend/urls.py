from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.login_view, name="login"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("attendance/", views.attendance_view, name="attendance"),

    # AJAX
    path("get-students/", views.get_students, name="get_students"),
    path("analytics-data/", views.attendance_analytics, name="attendance_analytics"),


    # AI Camera
    path(
        "camera-ai-detect/",
        views.camera_ai_detect,
        name="camera_ai_detect"
    ),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
