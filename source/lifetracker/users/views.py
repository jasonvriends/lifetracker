from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, UpdateView, TemplateView, RedirectView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect
from zoneinfo import available_timezones

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "pk"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None=None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()


class UserSettingsProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "pages/settings_profile.html"
    fields = ["first_name", "last_name", "timezone", "bio"]

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["timezones"] = sorted(available_timezones())
        return context

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("users:settings_profile")


class UserSettingsAccountView(LoginRequiredMixin, TemplateView):
    template_name = "pages/settings_account.html"


class UserSettingsAppearanceView(LoginRequiredMixin, TemplateView):
    template_name = "pages/settings/appearance.html"


class UserSettingsNotificationsView(LoginRequiredMixin, TemplateView):
    template_name = "pages/settings/notifications.html"


class UserSettingsDisplayView(LoginRequiredMixin, TemplateView):
    template_name = "pages/settings/display.html"


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('account_login')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Your account has been successfully deleted.")
        return super().delete(request, *args, **kwargs)
