from django.urls import path

from .views import (
    UserDetailView, UserSettingsProfileView, UserSettingsAccountView,
    UserSettingsAppearanceView, UserSettingsNotificationsView, UserSettingsDisplayView,
    UserDeleteView
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=UserDetailView.as_view(), name="redirect"),
    path("<int:pk>/", view=UserDetailView.as_view(), name="detail"),
    path("settings/", view=UserSettingsProfileView.as_view(), name="settings_profile"),
    path("settings/account/", view=UserSettingsAccountView.as_view(), name="settings_account"),
    path("settings/appearance/", view=UserSettingsAppearanceView.as_view(), name="settings_appearance"),
    path("settings/notifications/", view=UserSettingsNotificationsView.as_view(), name="settings_notifications"),
    path("settings/display/", view=UserSettingsDisplayView.as_view(), name="settings_display"),
    path("settings/delete/", view=UserDeleteView.as_view(), name="delete_account"),
]
