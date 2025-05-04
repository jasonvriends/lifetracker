from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("dashboard/", TemplateView.as_view(template_name="pages/dashboard.html"), name="dashboard"),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    path("journal/", TemplateView.as_view(template_name="pages/journal.html"), name="journal"),
    path("habits/", TemplateView.as_view(template_name="pages/habits.html"), name="habits"),
    path("goals/", TemplateView.as_view(template_name="pages/goals.html"), name="goals"),
    path("metrics/", TemplateView.as_view(template_name="pages/metrics.html"), name="metrics"),
    path("tasks/", TemplateView.as_view(template_name="pages/tasks.html"), name="tasks"),
    path("notes/", TemplateView.as_view(template_name="pages/notes.html"), name="notes"),
    path("settings/", TemplateView.as_view(template_name="pages/settings.html"), name="settings"),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("lifetracker.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),  # allauth doesn't support namespacing
    # Your stuff: custom urls includes go here
    # ...
]

# Media files (always serve in development)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Static files and debug toolbar (only in development)
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    
    # This allows the error pages to be debugged during development
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
