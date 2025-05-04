from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, UpdateView, TemplateView, RedirectView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from zoneinfo import available_timezones
import logging
from django.core.files.storage import default_storage
import os
from django.conf import settings
from django.core.files.base import ContentFile

User = get_user_model()
logger = logging.getLogger(__name__)


def validate_avatar(value):
    """Validate avatar file size and type."""
    max_size = 5 * 1024 * 1024  # 5MB
    if value.size > max_size:
        raise ValidationError(_('File size must be no more than 5MB.'))
    if not value.content_type.startswith('image/'):
        raise ValidationError(_('File must be an image.'))


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "pk"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["first_name", "last_name"]
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
    fields = ["first_name", "last_name", "timezone", "bio", "avatar"]

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["timezones"] = sorted(available_timezones())
        if self.request.user.avatar:
            logger.debug("Avatar URL: %s", self.request.user.avatar.url)
            logger.debug("Avatar path: %s", self.request.user.avatar.path)
        return context

    def form_valid(self, form):
        logger.debug("Form data: %s", form.cleaned_data)
        logger.debug("Files: %s", self.request.FILES)
        
        if 'avatar' in self.request.FILES:
            logger.debug("Avatar found in request.FILES")
            avatar_file = self.request.FILES['avatar']
            logger.debug("Avatar file name: %s", avatar_file.name)
            logger.debug("Avatar file size: %s", avatar_file.size)
            logger.debug("Avatar content type: %s", avatar_file.content_type)
            
            # Read a bit of the file to verify content
            content_start = avatar_file.read(100)
            logger.debug("Avatar file content: %s", content_start)
            avatar_file.seek(0)  # Reset file pointer after reading
            
            # Verify file is not empty
            if avatar_file.size == 0:
                logger.error("Avatar file is empty")
                form.add_error('avatar', "The uploaded file is empty")
                return self.form_invalid(form)
            
            try:
                validate_avatar(avatar_file)
                logger.debug("Avatar validation passed")
            except ValidationError as e:
                logger.error("Avatar validation failed: %s", e)
                form.add_error('avatar', e)
                return self.form_invalid(form)
            
            # Delete old avatar if it exists
            user = self.get_object()
            if user.avatar:
                logger.debug("Deleting old avatar")
                try:
                    old_path = user.avatar.path
                    logger.debug("Old avatar path: %s", old_path)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                        logger.debug("Successfully deleted old avatar file")
                except Exception as e:
                    logger.error("Error deleting old avatar: %s", e)
                
                # Clear the avatar field
                user.avatar = None
                user.save()
            
            # Manually handle the file upload
            from lifetracker.users.models import get_avatar_path
            
            # Generate the path
            path = get_avatar_path(user, avatar_file.name)
            logger.debug("Generated path for avatar: %s", path)
            
            # Save the file
            full_path = os.path.join(settings.MEDIA_ROOT, path)
            logger.debug("Full path for avatar: %s", full_path)
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # Save the file directly
            with open(full_path, 'wb+') as destination:
                for chunk in avatar_file.chunks():
                    destination.write(chunk)
            
            # Verify file was saved
            if os.path.exists(full_path):
                file_size = os.path.getsize(full_path)
                logger.debug("File saved successfully. Size: %s bytes", file_size)
                if file_size == 0:
                    logger.error("Saved file has 0 bytes!")
            else:
                logger.error("File was not saved at %s", full_path)
            
            # Update the model
            user.avatar = path
            logger.debug("Setting user avatar to: %s", path)
            
            # Update the form
            form.instance.avatar = path
        
        try:
            # Save the form
            self.object = form.save()
            logger.debug("Form saved successfully")
            
            if self.object.avatar:
                logger.debug("New avatar details:")
                logger.debug("- Name: %s", self.object.avatar.name)
                logger.debug("- URL: %s", self.object.avatar.url)
                logger.debug("- Path: %s", self.object.avatar.path)
                if os.path.exists(self.object.avatar.path):
                    logger.debug("- Size: %s", os.path.getsize(self.object.avatar.path))
                    logger.debug("File exists at the expected path")
                else:
                    logger.error("File does not exist at path: %s", self.object.avatar.path)
            else:
                logger.debug("No avatar set after save")
            
            messages.success(self.request, "Profile updated successfully.")
            return super().form_valid(form)
        except Exception as e:
            logger.error("Error saving form: %s", e)
            form.add_error(None, "Error saving profile. Please try again.")
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("users:settings_profile")

    def post(self, request, *args, **kwargs):
        if 'delete_avatar' in request.POST:
            user = self.get_object()
            if user.avatar:
                try:
                    # Get the file path before deleting
                    avatar_path = user.avatar.path
                    logger.debug("Deleting avatar at path: %s", avatar_path)
                    # Delete the file from storage if it exists
                    if os.path.exists(avatar_path):
                        os.remove(avatar_path)
                        logger.debug("Successfully deleted avatar file")
                    user.avatar = None
                    user.save()
                    return JsonResponse({'status': 'success'})
                except Exception as e:
                    logger.error("Error deleting avatar: %s", e)
                    return JsonResponse({'status': 'error', 'message': str(e)})
            return JsonResponse({'status': 'error', 'message': 'No avatar to delete'})
        return super().post(request, *args, **kwargs)


class UserSettingsAccountView(LoginRequiredMixin, TemplateView):
    template_name = "pages/settings_account.html"


class UserSettingsAppearanceView(LoginRequiredMixin, TemplateView):
    template_name = "pages/settings/appearance.html"


class UserSettingsNotificationsView(LoginRequiredMixin, TemplateView):
    template_name = "pages/settings/notifications.html"


class UserSettingsDisplayView(LoginRequiredMixin, TemplateView):
    template_name = "pages/settings_display.html"
    
    def post(self, request, *args, **kwargs):
        user = request.user
        theme = request.POST.get('theme', '')
        
        # Empty string means use system default (light/dark)
        user.theme = theme if theme else None
        user.save()
        
        messages.success(request, _("Display settings updated successfully."))
        return redirect(reverse("users:settings_display"))


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('account_login')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Your account has been successfully deleted.")
        return super().delete(request, *args, **kwargs)
